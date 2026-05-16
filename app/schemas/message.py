from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class CommunityMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: str
    user_id: int
    user_name: str
    text: str
    created_at: datetime
    user_profile_image_url: Optional[str] = None


class CommunityMessageCreate(BaseModel):
    room_id: str = Field(default="general", max_length=50)
    text: str = Field(min_length=1, max_length=2000)
