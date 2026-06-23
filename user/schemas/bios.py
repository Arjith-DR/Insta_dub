from pydantic import BaseModel
from typing import Optional

class BioCreate(BaseModel):
    user_id: int
    text: str
    current: Optional[bool] = True

class BioOut(BaseModel):
    bio_id: int
    user_id: int
    b_txt: str
    current: bool

    class Config:
        from_attributes = True
