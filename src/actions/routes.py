from fastapi import APIRouter
from typing import List

from .new_issues_importer import NewIssuesImporter
from ..models.issue import IssueModel
from ..utils.db_connection import db_prediction_mechanism

router = APIRouter()

@router.get("/import_new_issues/", 
            response_description="Import new Issues",
            tags=["actions"])
async def import_new_issues():
    new_issues_importer = NewIssuesImporter()
    return await new_issues_importer.import_new_issues()