from bson import ObjectId
from pydantic import BaseModel

class DefaultModel(BaseModel):
    def convert_to_dict(self):
        result = {k: v for k, v in self.dict().items() \
            if v is not None}

        return result

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}