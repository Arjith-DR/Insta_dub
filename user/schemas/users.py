from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    role_id: int
    email: EmailStr
    password: str
    status: Optional[str] = "active"

class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class UsernameChange(BaseModel):
    user_id: int
    new_username: str

class UsernameOut(BaseModel):
    user_name_id: int
    user_id: int
    user_status: str
    current: bool

    class Config:
        from_attributes = True

class PasswordChangeOut(BaseModel):
    change_id: int
    user_id: int
    old_password: str
    new_password: str

    class Config:
        from_attributes = True
