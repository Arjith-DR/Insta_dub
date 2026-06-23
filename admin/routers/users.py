from fastapi import APIRouter, HTTPException, Depends
from admin.schemas import AdminUserOut, AdminResetPassword
from admin.crud.users import (
    admin_list_users,
    admin_hard_delete_user,
    admin_activate_user,
    admin_deactivate_user,
    admin_reset_password,
)
from core.security import get_current_admin_user


admin_users_router = APIRouter(prefix="/admin/users", tags=["admin-users"])


@admin_users_router.get("/", response_model=list[AdminUserOut])
async def list_all_users(current_user=Depends(get_current_admin_user)):
    return await admin_list_users()


@admin_users_router.delete("/{user_id}")
async def hard_delete_user(user_id: int, current_user=Depends(get_current_admin_user)):
    deleted = await admin_hard_delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User permanently deleted"}


@admin_users_router.put("/{user_id}/activate", response_model=AdminUserOut)
async def activate_user(user_id: int, current_user=Depends(get_current_admin_user)):
    user = await admin_activate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@admin_users_router.put("/{user_id}/deactivate", response_model=AdminUserOut)
async def deactivate_user(user_id: int, current_user=Depends(get_current_admin_user)):
    user = await admin_deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@admin_users_router.put("/{user_id}/reset-password", response_model=AdminUserOut)
async def reset_password(user_id: int, body: AdminResetPassword, current_user=Depends(get_current_admin_user)):
    user = await admin_reset_password(user_id, body.new_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
