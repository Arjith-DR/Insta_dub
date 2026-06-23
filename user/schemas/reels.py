from pydantic import BaseModel
from typing import Optional

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
    like_id: int
    reel_id: int
    user_id: int
    is_liked: bool

    class Config:
        from_attributes = True
