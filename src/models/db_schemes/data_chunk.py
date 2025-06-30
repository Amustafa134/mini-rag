from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId  # or your custom ObjectId validator

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")  # Use alias for MongoDB
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId
    chunk_asset_id: ObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("chunk_project_id", 1),  # Index for chunk_project_id
                ],
                "name": "chunk_project_id_index_1",
                "unique": False,  # Ensure chunk_project_id is not unique
            }
        ]
