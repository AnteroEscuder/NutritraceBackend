from pydantic import BaseModel, Field
from datetime import datetime


class CommunityMessageOut(BaseModel):
    id: int
    room_id: str
    user_id: int
    user_name: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2


class CommunityMessageCreate(BaseModel):
    room_id: str = Field(default="general", max_length=50)
    text: str = Field(min_length=1, max_length=2000)
