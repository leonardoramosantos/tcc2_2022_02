from datetime import datetime as date_type
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

from ..utils.py_object_id import PyObjectId

class ConfigurationModel(BaseModel):
    """
    DTO for Configuration on Database

    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cfg_key: str = Field()
    cfg_value: str = Field()

class UpdateConfigurationModel(BaseModel):
    """
    DTO for Inserting/Updating Configuration on Database

    """

    cfg_key: Optional[str]
    cfg_value: Optional[str]