from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class PostCreate(BaseModel):
    user_id: int
    caption: str
    status: Optional[str] = "active"

class PostOut(BaseModel):
    post_id: int
    user_id: int
    caption: str
    status: str

    class Config:
        from_attributes = True

class PostCommentCreate(BaseModel):
    post_id: int
    user_id: int
    text: str

class PostCommentOut(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    text: str

    class Config:
        from_attributes = True

class PostLikeOut(BaseModel):
    content_type: str                
    content_id: str                  
    content_owner_user_id: int       
    liked_by_user_id: int            
    liked_at: datetime
 

class PostMediaCreate(BaseModel):
    post_id: int
    media_url: str
    media_type: str
    order_index: int

class PostMediaOut(BaseModel):
    media_id: int
    post_id: int
    media_url: str
    media_type: str
    order_index: int

    class Config:
        from_attributes = True
