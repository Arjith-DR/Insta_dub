from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

class ReelCreate(BaseModel):
    user_id: int
    video_url: str
    caption: str
    status: Optional[str] = "active"

class ReelOut(BaseModel):
    reel_id: int
    user_id: int
    video_url: str
    caption: str
    status: str
    likes: int = 0

    class Config:
        from_attributes = True

class ReelCommentCreate(BaseModel):
    reel_id: int
    user_id: int
    text: str

class ReelCommentOut(BaseModel):
    comment_id: int
    reel_id: int
    user_id: int
    text: str

    class Config:
        from_attributes = True

class ReelLikeOut(BaseModel):
    content_type: Optional[str] = None
    reel_id: Optional[int] = None
    content_owner_user_id: Optional[int] = None
    liked_by_user_id: Optional[int] = None
    liked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
