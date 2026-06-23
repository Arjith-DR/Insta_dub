from pydantic import BaseModel


class PrivacyUpdate(BaseModel):
    user_id: int
    new_status: str


class PrivacyOut(BaseModel):
    priv_id: int
    user_id: int
    priv_status: str
    current: bool

    class Config:
        from_attributes = True
