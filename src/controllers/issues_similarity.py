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