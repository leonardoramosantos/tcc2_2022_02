from bson import ObjectId
from datetime import datetime as date_type
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

from ..utils.py_object_id import PyObjectId

class IssueModel(BaseModel):
    """
    DTO for Issues on Database

    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    issue_id: int = Field()
    project_id: int = Field()
    issue_type: str = Field()
    subject: str = Field()
    description: str = Field()
    created_on: date_type = Field()
    closed_on: Optional[date_type]
    updated_on: date_type = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateIssueModel(BaseModel):
    """
    """

    issue_id: Optional[int]
    project_id: Optional[int]
    issue_type: Optional[str]
    subject: Optional[str]
    description: Optional[str]
    created_on: Optional[date_type]
    closed_on: Optional[date_type]
    updated_on: Optional[date_type]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}