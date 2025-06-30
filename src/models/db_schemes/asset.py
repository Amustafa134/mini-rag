from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime, timezone


utc_now = datetime.now(timezone.utc)


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")  # Use alias for MongoDB
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(gt=0, default=None)  # Size in bytes
    asset_config: dict = Field(default=None)
    asset_pushed_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    
    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("asset_project_id", 1) # Index for asset_project_id
                ],  
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key": [
                    ("asset_project_id", 1),    # Composite index for asset_type and asset_name
                    ("asset_name", 1)
                ],  
                "name": "asset_project_id_name_index_1",
                "unique": True  # Ensure unique combination of asset_type and asset_name
            }
        ]

