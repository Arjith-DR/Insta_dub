from fastapi import APIRouter, HTTPException, Depends
from admin.schemas import RoleCreate, RoleOut, UserRoleAssign, UserRoleOut
from admin.crud.roles import (
    create_role,
    get_roles,
    assign_role_to_user,
    remove_role_from_user,
    get_user_roles,
)
from core.security import get_current_admin_user


admin_roles_router = APIRouter(prefix="/admin/roles", tags=["admin-roles"])


@admin_roles_router.post("/", response_model=RoleOut)
async def create_new_role(role: RoleCreate, current_user=Depends(get_current_admin_user)):
    return await create_role(role.role_name, role.description)


@admin_roles_router.get("/", response_model=list[RoleOut])
async def list_roles(current_user=Depends(get_current_admin_user)):
    return await get_roles()


@admin_roles_router.post("/assign", response_model=UserRoleOut)
async def assign_role(assignment: UserRoleAssign, current_user=Depends(get_current_admin_user)):
    return await assign_role_to_user(assignment.user_id, assignment.role_id)


@admin_roles_router.delete("/remove")
async def remove_role(assignment: UserRoleAssign, current_user=Depends(get_current_admin_user)):
    removed = await remove_role_from_user(assignment.user_id, assignment.role_id)
    if not removed:
        raise HTTPException(status_code=404, detail="User role assignment not found")
    return {"detail": "Role removed from user"}


@admin_roles_router.get("/user/{user_id}", response_model=list[RoleOut])
async def list_user_roles(user_id: int, current_user=Depends(get_current_admin_user)):
    return await get_user_roles(user_id)
