from fastapi import APIRouter
from typing import List

from ..models.issue import IssueModel
from ..utils.db_connection import db_prediction_mechanism

router = APIRouter()

@router.get("/issues/", response_description="List all Issues",
            response_model=List[IssueModel], tags=["internal"])
async def issues():
    return await db_prediction_mechanism["issue"].find().to_list(1000)