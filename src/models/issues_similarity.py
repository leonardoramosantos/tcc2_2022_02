from bson import ObjectId
from datetime import datetime as date_type
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from typing import List

from ..utils.py_object_id import PyObjectId

class IssuesSimilarityModel(BaseModel):
    """
    DTO for issues similarities on Database

    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    issues: List[PyObjectId] = Field()
    similarity_relevance: float = Field()
    updated_on: date_type = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UpdateIssuesSimilarityModel(BaseModel):
    """
    """

    issues: List[PyObjectId]
    similarity_relevance: Optional[float]
    updated_on: Optional[date_type]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }