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
    content_type: str             
    content_id: str                
    content_owner_user_id: int  
    liked_by_user_id: int         
    liked_at: datetime 
