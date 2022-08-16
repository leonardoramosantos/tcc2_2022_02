from datetime import datetime
from datetime import timedelta

from .redmine_wrappers.updated_issues import RedmineUpdatedIssuesWrapper
from .similarity_processor import SimilarityProcessor
from ..controllers.configuration import ConfigurationController
from ..controllers.issue import IssueController
from ..controllers.issues_similarity import IssuesSimilarityController
from ..models.issue import IssueModel
from ..models.issue import UpdateIssueModel
from ..utils.constants import CFG_KEY_LAST_UPDATED_ISSUE_DATE_TIME

class UpdatedIssuesImporter():
    async def import_updated_issues_and_process_similarities(self, last_date_time=None):
        result = []
        last_imported_date_time = None
        issue_controller = IssueController()

        wrapper = RedmineUpdatedIssuesWrapper()
        issues = await wrapper.get_updated_issues(last_date_time)

        for issue in issues:
            uptd_issue = UpdateIssueModel(
                issue_id=issue.get("id"),
                project_id=issue.get("project", {}).get("id"),
                issue_type=issue.get("tracker", {}).get("name"),
                subject=issue.get("subject"),
                description=issue.get("description"),
                created_on=issue.get("created_on"),
                closed_on=issue.get("closed_on"),
                updated_on=issue.get("updated_on"))
            rslt_issue = await issue_controller.save_issue(uptd_issue.issue_id,
                                                           uptd_issue)
            rslt_issue = IssueModel.parse_obj(rslt_issue)

            last_imported_date_time = datetime.strptime(issue.get("updated_on"),
                                               "%Y-%m-%dT%H:%M:%SZ")
            # Adds 1 second to save next datetime to search
            last_imported_date_time = last_imported_date_time + timedelta(seconds=1)

            result.append(rslt_issue)

            similarity_processor = SimilarityProcessor()
            await similarity_processor.process_issue_similarities(rslt_issue)

        if last_imported_date_time is not None:
            cfg_controller = ConfigurationController()
            await cfg_controller.save_configuration(CFG_KEY_LAST_UPDATED_ISSUE_DATE_TIME, 
                                                    last_imported_date_time)

        return result