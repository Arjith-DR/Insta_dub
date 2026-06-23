from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdminPrivacyOverrideCreate(BaseModel):
    user_id: Optional[int] = None
    policy_name: Optional[str] = None
    policy_value: str
    reason: Optional[str] = None


class AdminPrivacyOverrideOut(BaseModel):
    override_id: int
    user_id: Optional[int]
    policy_name: Optional[str]
    policy_value: str
    reason: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdminGlobalPrivacyPolicyCreate(BaseModel):
    policy_name: str
    policy_value: str


class AdminGlobalPrivacyPolicyOut(BaseModel):
    override_id: int
    policy_name: Optional[str]
    policy_value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
