from pydantic import BaseModel
from typing import Optional


class SavedCategoryCreate(BaseModel):
    user_id: int
    name: str


class SavedCategoryOut(BaseModel):
    category_id: int
    user_id: int
    name: str

    class Config:
        from_attributes = True


class SavedItemCreate(BaseModel):
    user_id: int
    content_id: int
    category_id: Optional[int] = None


class SavedItemOut(BaseModel):
    saved_id: int
    user_id: int
    content_id: int
    category_id: Optional[int]
    is_saved: bool

    class Config:
        from_attributes = True
