from fastapi import APIRouter
from fastapi import Body
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List

from ..models.issue import IssueModel
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