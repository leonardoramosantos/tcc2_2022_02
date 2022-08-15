from datetime import datetime
from datetime import timedelta

from ..models.issue import UpdateIssueModel
from ..controllers.configuration import ConfigurationController
from ..controllers.issue import IssueController
from ..utils.constants import CFG_KEY_LAST_ISSUE_DATE_TIME
from .redmine_wrappers.new_issues import RedmineNewIssuesWrapper

class NewIssuesImporter():
    async def import_new_issues(self):
        result = []
        last_date_time = None
        issue_controller = IssueController()

        wrapper = RedmineNewIssuesWrapper()
        issues = await wrapper.get_new_issues()

        for issue in issues:
            new_issue = UpdateIssueModel(
                issue_id=issue.get("id"),
                project_id=issue.get("project", {}).get("id"),
                subject=issue.get("subject"),
                description=issue.get("description"),
                created_on=issue.get("created_on"),
                closed_on=issue.get("closed_on"),
                updated_on=issue.get("updated_on")
                )
            await issue_controller.save_issue(new_issue.issue_id, new_issue)

            last_date_time = datetime.strptime(issue.get("created_on"),
                                               "%Y-%m-%dT%H:%M:%SZ")
            # Adds 1 second to save next datetime to search
            last_date_time = last_date_time + timedelta(seconds=1)

            result.append(new_issue)

        if last_date_time is not None:
            cfg_controller = ConfigurationController()
            await cfg_controller.save_configuration(CFG_KEY_LAST_ISSUE_DATE_TIME, 
                                                    last_date_time)

        return result