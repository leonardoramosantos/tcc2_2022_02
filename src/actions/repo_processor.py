from ..controllers.issue_commit import IssueCommitController
from ..controllers.project import ProjectController
from ..models.project import ProjectModel
from ..models.project import REPO_TYPE_GIT_CODE
from ..models.project import REPO_TYPE_SVN_CODE
from ..utils.db_connection import db_prediction_mechanism
from ..utils.git_wrapper import GitWrapper
from ..utils.svn_wrapper import SVNWrapper

class RepoProcessor:
    def __init__(self):
        self.project_id = None
        self.project_obj = None

    async def load_project(self, project_id):
        self.project_id = project_id

        project_filter = {
            "project_id": project_id
        }
        project_obj = await db_prediction_mechanism['project'].find_one(project_filter)
        self.project_obj = ProjectModel(**project_obj)

        if self.project_obj.repo_type == REPO_TYPE_GIT_CODE:
            self.repo_wrapper = GitWrapper(self.project_obj.repo_path,
                                           self.project_obj.repo_last_commit)
        elif self.project_obj.repo_type == REPO_TYPE_SVN_CODE:
            self.repo_wrapper = SVNWrapper(self.project_obj.repo_path,
                                           self.project_obj.repo_last_commit)
        else:
            self.repo_wrapper = None

    async def update_repo(self, project_id):
        if self.project_obj is None:
            await self.load_project(project_id)

        last_commit, issue_commits = await self.repo_wrapper.udpate_repo()
        if last_commit is not None:
            self.project_obj.repo_last_commit = last_commit

            controller = ProjectController()
            await controller.save_existing_project(self.project_obj)

        commit_controller = IssueCommitController()
        for issue_commit in issue_commits:
            await commit_controller.save_issue_commit(issue_commit)

        result = {
            "last_commit": last_commit,
            "issue_commits": issue_commits
        }
        return result
        #svn co http://effe371eb6e3:18080/svn/project_2 project_2 --username=admin