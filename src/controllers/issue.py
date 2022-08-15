from ..utils.db_connection import db_prediction_mechanism

class IssueController():
    """
    Wrapper to operate on the Database using Models

    """
    
    def __init__(self):
        self.cfg_collection = db_prediction_mechanism["issue"]

    async def save_issue(self, issue_id, issue_to_save):
        result = None
        
        issue_to_save = {k: v for k, v in issue_to_save.dict().items() \
            if v is not None}

        issue_filter = {
            "issue_id": issue_id
        }

        issue_update = {
            "$set": issue_to_save
        }

        result = await self.cfg_collection.update_one(issue_filter,
                                                      issue_update,
                                                      True)

        return result.raw_result