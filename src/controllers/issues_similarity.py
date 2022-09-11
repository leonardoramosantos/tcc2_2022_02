from .issue_commit import IssueCommitController
from .issue import IssueController
from ..models.issue import IssueStatusEnum
from ..utils.constants import MAX_SIMILARITIES_RETURNED
from ..utils.db_connection import db_prediction_mechanism

class IssuesSimilarityController():
    """
    Wrapper to operate on the Database using Models

    """

    def __init__(self):
        self.similarities_collec = db_prediction_mechanism["issues_similarity"]

    async def save_issues_similarity(self, issues_set, similarity_to_save):
        similarity_to_save = {k: v for k, v in similarity_to_save.dict().items() \
            if v is not None}

        issues_filter = {
            "issues": issues_set
        }

        similarity_update = {
            "$set": similarity_to_save
        }

        await self.similarities_collec.update_one(issues_filter,
                                                  similarity_update,
                                                  True)

        return await self.similarities_collec.find_one(issues_filter)

    async def get_most_similars_issues(self, issue):
        issue_filter = {
            "issues": {
                "$in": [issue.id]
            }
        }

        return await self.similarities_collec.find(issue_filter).sort(
            "similarity_relevance", -1).to_list(MAX_SIMILARITIES_RETURNED)

    async def get_most_similar_issues_dict(self, issue, issue_status_filter:IssueStatusEnum=IssueStatusEnum.ALL):
        result = []
        issue_controller = IssueController()
        issue_filter = {
            "issues": {
                "$in": [issue.id]
            }
        }

        similarities = await self.similarities_collec.find(issue_filter).sort(
            "similarity_relevance", -1).to_list(1000)

        for similar in similarities:
            if len(result) < MAX_SIMILARITIES_RETURNED:
                issue_mongo_id = None
                for issue_similarity_mongo_id in similar["issues"]:
                    if issue_similarity_mongo_id != issue.id:
                        issue_mongo_id = issue_similarity_mongo_id
                    
                similar_issue = await issue_controller.get_issue_by_issue_mongo_id(issue_mongo_id)
                if issue_status_filter == IssueStatusEnum.ALL or \
                        ((issue_status_filter == IssueStatusEnum.ONLY_OPEN) and (similar_issue.closed_on is None)) or \
                        ((issue_status_filter == IssueStatusEnum.ONLY_CLOSED) and (similar_issue.closed_on is not None)):
                    result.append((similar_issue, similar["similarity_relevance"]))
        return result

    async def get_most_similar_open_issues(self, issue):
        return await self.get_most_similar_issues_dict(issue, IssueStatusEnum.ONLY_OPEN)

    async def get_most_similar_closed_issues(self, issue):
        return await self.get_most_similar_issues_dict(issue, IssueStatusEnum.ONLY_CLOSED)

    async def get_and_process_issue_artifacts(self, issue):
        result = []
        commit_controller = IssueCommitController()

        similarities = await self.get_most_similar_closed_issues(issue)
        for similarity, relevance in similarities:
            commits = await commit_controller.get_all_issue_commits(similarity.issue_id)
            for commit in commits:
                for file in commit["changes"]:
                    result.append({ "file_name": file["file_name"] })

        return result

    async def get_issue_similarities_and_artifacts(self, issue_similarity):
        result = []
        issue_controller = IssueController()

        similar_issues = await self.get_most_similar_open_issues(issue_similarity)
        
        for issue, relevance in similar_issues:
            issue_obj = issue.convert_to_dict()
            issue_obj.pop("id")
            issue_obj["similarity_relevance"] = relevance

            issue_obj["artifacts"] = await self.get_and_process_issue_artifacts(issue)
            result.append(issue_obj)

        return result