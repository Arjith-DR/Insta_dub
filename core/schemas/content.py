from pydantic import BaseModel
from typing import Optional


class ContentCreate(BaseModel):
    user_id: int
    type: str
    status: Optional[str] = "active"


class ContentOut(BaseModel):
    content_id: int
    user_id: int
    type: str
    status: str

    class Config:
        from_attributes = True
