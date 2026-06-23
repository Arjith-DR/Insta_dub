from fastapi import APIRouter, HTTPException, Depends
from admin.schemas import (
    AdminPrivacyOverrideCreate,
    AdminPrivacyOverrideOut,
    AdminGlobalPrivacyPolicyCreate,
    AdminGlobalPrivacyPolicyOut,
)
from admin.crud.privacy import (
    admin_override_user_privacy,
    admin_get_all_privacy_overrides,
    admin_create_global_privacy_policy,
    admin_get_global_privacy_policies,
)
from core.security import get_current_admin_user


admin_privacy_router = APIRouter(prefix="/admin/privacy", tags=["admin-privacy"])


@admin_privacy_router.put("/user/{user_id}", response_model=AdminPrivacyOverrideOut)
async def override_user_privacy(user_id: int, body: AdminPrivacyOverrideCreate, current_user=Depends(get_current_admin_user)):
    override = await admin_override_user_privacy(user_id, body.policy_value, body.reason)
    return override


@admin_privacy_router.get("/overrides", response_model=list[AdminPrivacyOverrideOut])
async def list_privacy_overrides(current_user=Depends(get_current_admin_user)):
    return await admin_get_all_privacy_overrides()


@admin_privacy_router.post("/global", response_model=AdminGlobalPrivacyPolicyOut)
async def create_global_policy(body: AdminGlobalPrivacyPolicyCreate, current_user=Depends(get_current_admin_user)):
    return await admin_create_global_privacy_policy(body.policy_name, body.policy_value)


@admin_privacy_router.get("/global", response_model=list[AdminGlobalPrivacyPolicyOut])
async def list_global_policies(current_user=Depends(get_current_admin_user)):
    return await admin_get_global_privacy_policies()
