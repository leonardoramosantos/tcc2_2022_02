from ..utils.db_connection import db_prediction_mechanism

class IssueController():
    """
    Wrapper to operate on the Database using Models

    """

    def __init__(self):
        self.similarities_collec = db_prediction_mechanism["issue"]

    async def save_issue(self, issue_id, issue_to_save):
        issue_to_save = {k: v for k, v in issue_to_save.dict().items() \
            if v is not None}

        issue_filter = {
            "issue_id": issue_id
        }

        issue_update = {
            "$set": issue_to_save
        }

        await self.similarities_collec.update_one(issue_filter,
                                             issue_update,
                                             True)

        return await self.similarities_collec.find_one(issue_filter)

    async def get_all_issues(self):
        return await self.similarities_collec.find().to_list(100000)

    async def get_all_issues_from_project(self, project_id):
        issue_filter = {
            "project_id": project_id
        }

        return await self.similarities_collec.find().to_list(100000)

    async def get_issue_by_issue_id(self, issue_id):
        issue_filter = {
            "issue_id": issue_id
        }
        result = await self.similarities_collec.find_one(issue_filter)

        return result