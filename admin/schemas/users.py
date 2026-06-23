from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class AdminUserOut(BaseModel):
    user_id: int
    email: EmailStr
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdminResetPassword(BaseModel):
    new_password: str


class AdminActivateDeactivate(BaseModel):
    status: str  # "active" or "inactive"
