from fastapi import APIRouter
from fastapi import Body
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List

from ..controllers.issue import IssueController
from ..controllers.issue_commit import IssueCommitController
from ..controllers.issues_similarity import IssuesSimilarityController
from ..models.issue import IssueModel
from ..models.issue_commit import IssueCommitModel
from ..models.issues_similarity import IssuesSimilarityModel
from ..models.project import ProjectModel
from ..models.project import UpdateProjectModel
from ..utils.db_connection import db_prediction_mechanism

router = APIRouter()

@router.get("/issue/", response_description="List all Issues",
            response_model=List[IssueModel], tags=["internal"])
async def issue():
    return await db_prediction_mechanism["issue"].find().to_list(1000)

@router.get("/issues_similarity/",
            response_description="List Most Similar Issues",
            response_model=List[IssuesSimilarityModel], tags=["internal"])
async def issues_similarity():
    return await db_prediction_mechanism["issues_similarity"].find().to_list(1000)

@router.get("/project/", response_description="List all Projects",
            response_model=List[ProjectModel], tags=["internal"])
async def project():
    return await db_prediction_mechanism["project"].find().to_list(1000)

# Ajustar - Não está funcionando corretamente
@router.post("/project/", response_description="Insert a Project",
             response_model=ProjectModel, tags=["internal"])
async def insert_project(project: UpdateProjectModel = Body(...)):
    project_obj = jsonable_encoder(project)
    new_project = await db_prediction_mechanism["project"].insert_one(project_obj)
    created_project = await db_prediction_mechanism["project"].find_one({"_id": new_project.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=ProjectModel(created_project))

@router.get("/issue_commits/", response_description="Lista Issue Commits",
            tags=["internal"], response_model=List[IssueCommitModel])
async def get_issue_commits(issue_id: int):
    controller = IssueCommitController()
    return await controller.get_all_issue_commits(issue_id)

@router.post("/issue_similarities_and_artifacts/", response_description="Get Similar Issues and Artifacts",
             tags=["internal", "integration"])
async def get_issue_similarities_and_artifacts(issue_id: int):
    issue_controller = IssueController()
    issue = await issue_controller.get_issue_by_issue_id(issue_id)
    controller = IssuesSimilarityController()
    return await controller.get_issue_similarities_and_artifacts(issue)