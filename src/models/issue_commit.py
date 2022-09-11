from bson import ObjectId
from datetime import datetime as date_type
from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional
from typing import Union

from .default_model import DefaultModel
from ..utils.py_object_id import PyObjectId


class IssueCommitFileModel(BaseModel):
    """
    """

    file_name: str = Field()
    changes: List[str] = Field()

class IssueCommitModel(DefaultModel):
    """
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    issue_id: int = Field()
    commit_id: str = Field()
    message: str = Field()
    username: str = Field()

    changes: List[IssueCommitFileModel] = Field()