from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

from ..utils.py_object_id import PyObjectId

REPO_TYPE_GIT="git"
REPO_TYPE_SVN="svn"
REPO_TYPES = {
    REPO_TYPE_GIT: 0,
    REPO_TYPE_SVN: 1
}
REPO_TYPE_GIT_CODE = REPO_TYPES[REPO_TYPE_GIT]
REPO_TYPE_SVN_CODE = REPO_TYPES[REPO_TYPE_SVN]

class ProjectModel(BaseModel):
    """
    DTO for Projects on Database

    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    project_id: int = Field()
    name: str = Field()
    repo_url: Optional[str]
    repo_path: Optional[str]
    repo_type: Optional[int]
    repo_initialized: Optional[bool]
    repo_last_commit: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateProjectModel(BaseModel):
    """
    """

    project_id: Optional[int]
    name: Optional[str]
    repo_url: Optional[str]
    repo_path: Optional[str]
    repo_type: Optional[int]
    repo_initialized: Optional[bool]
    repo_last_commit: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}