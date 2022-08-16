from fastapi import APIRouter
from typing import List

from .new_issues_importer import NewIssuesImporter
from .similarity_processor import SimilarityProcessor
from .updated_issues_importer import UpdatedIssuesImporter
from ..controllers.issues_similarity import IssuesSimilarityController
from ..models.issue import IssueModel
from ..models.issues_similarity import IssuesSimilarityModel
from ..utils.db_connection import db_prediction_mechanism

router = APIRouter()

@router.get("/import_new_issues/", 
            response_description="Import new Issues",
            tags=["actions"],
            response_model=List[IssueModel])
async def import_new_issues():
    importer = NewIssuesImporter()
    return await importer.import_new_issues_and_process_similarities()

@router.get("/import_updated_issues/",
            response_description="Import updated Issues",
            tags=["actions"],
            response_model=List[IssueModel])
async def import_updated_issues():
    importer = UpdatedIssuesImporter()
    return await importer.import_updated_issues_and_process_similarities()

@router.get("/process_issue_similarities/{issue_id}",
            response_description="Process Issue Similarities",
            tags=["actions"], response_model=List[IssuesSimilarityModel])
async def reprocess_issue(id: int):
    similarity_processor = SimilarityProcessor()
    processed_data = await similarity_processor.process_issue_similarities_by_id(id)

    similarity_controller = IssuesSimilarityController()
    return await similarity_controller.get_most_similars_issues(
            processed_data.get("issue_processed"))
