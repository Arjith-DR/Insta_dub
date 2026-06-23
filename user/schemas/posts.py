from pydantic import BaseModel
from typing import Optional

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
    like_id: int
    post_id: int
    user_id: int
    is_liked: bool

    class Config:
        from_attributes = True

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
