import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from ..controllers.issue import IssueController
from ..controllers.issues_similarity import IssuesSimilarityController
from ..models.issue import IssueModel
from ..models.issues_similarity import UpdateIssuesSimilarityModel
from ..utils.constants import ISSUE_TEXT_SEPARATOR

class SimilarityProcessor():
    def __init__(self):
        self.similarity_controller = IssuesSimilarityController()
        self.issue_controller = IssueController()

    async def process_issue_similarities_by_id(self, issue_id):
        issue = await self.issue_controller.get_issue_by_issue_id(issue_id)

        return await self.process_issue_similarities(issue)

    async def process_issue_similarities(self, issue_to_process):
        result = {}
        result["issue_processed"] = issue_to_process

        issue_list = None 
        if os.environ.get("PROCESS_ALL_PROJECTS") == "S":
            issue_list = await self.issue_controller.get_all_issues()
        else:
            issue_list = await self.issue_controller.get_all_issues_from_project(
                issue_to_process.project_id)

        count_processed = 0
        for issue in issue_list:
            if issue.get("_id") != issue_to_process.id:
                issue_to_compare = IssueModel.parse_obj(issue)

                # Necessary because if not sorted will change order and
                # insert a new document every time
                issues_set = self.__sort_object_ids(issue_to_process, issue_to_compare)

                rslt_relevance = self.__calculate_similarity(issue_to_process,
                                                             issue_to_compare)

                similarity_to_save = UpdateIssuesSimilarityModel(
                    issues=issues_set,
                    similarity_relevance=rslt_relevance,
                    updated_on=datetime.now()
                )

                await self.similarity_controller.save_issues_similarity(issues_set,
                                                                        similarity_to_save)
                count_processed = count_processed + 1

        result["count_processed"] = count_processed

        return result

    def __calculate_similarity(self, first_issue, second_issue):
        str_first_issue = [(first_issue.issue_type + ISSUE_TEXT_SEPARATOR + \
            first_issue.subject + ISSUE_TEXT_SEPARATOR + first_issue.description).lower()]
        str_second_issue = [(second_issue.issue_type + ISSUE_TEXT_SEPARATOR + \
            second_issue.subject + ISSUE_TEXT_SEPARATOR + second_issue.description).lower()]

        doc_vectors = TfidfVectorizer().fit_transform(str_first_issue + str_second_issue)
        cosine_similarities = linear_kernel(doc_vectors[0:1], doc_vectors).flatten()
        ts_perc = cosine_similarities[1]

        return ts_perc

    def __sort_object_ids(self, issue_1, issue_2):
        result = []
        objs_set = set({int.from_bytes(issue_1.id.binary, "big"), 
                        int.from_bytes(issue_2.id.binary, "big")})

        for i in objs_set:
            if int.from_bytes(issue_1.id.binary, "big") == i:
                result.append(issue_1.id)
            else:
                result.append(issue_2.id)

        return result