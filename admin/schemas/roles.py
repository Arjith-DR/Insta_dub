from pydantic import BaseModel
from typing import Optional


class RoleCreate(BaseModel):
    role_name: str
    description: Optional[str] = None


class RoleOut(BaseModel):
    role_id: int
    role_name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class UserRoleAssign(BaseModel):
    user_id: int
    role_id: int


class UserRoleOut(BaseModel):
    user_role_id: int
    user_id: int
    role_id: int

    class Config:
        from_attributes = True
