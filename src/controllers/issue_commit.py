from typing import List
from ..models.issue_commit import IssueCommitModel
from ..utils.db_connection import db_prediction_mechanism

class IssueCommitController():
    """
    """

    def __init__(self):
        self.issue_commit_collec = db_prediction_mechanism["issue_commit"]

    async def save_issue_commit(self, issue_commit_to_save):
        issue_commit_to_save = {k: v for k, v in issue_commit_to_save.dict().items() \
            if v is not None}

        await self.issue_commit_collec.insert_one(issue_commit_to_save)

    async def get_all_issue_commits(self, issue_id) -> List[IssueCommitModel]:
        issue_filter = {
            "issue_id": issue_id
        }

        return await self.issue_commit_collec.find(issue_filter).to_list(1000)