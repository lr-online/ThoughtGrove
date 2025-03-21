from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer

class BaseDocument(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat() 