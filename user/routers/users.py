from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from user.schemas import UserCreate, UserOut, UsernameOut, PasswordChangeOut

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    return await dispatch("user", "create", user.role_id, user.email, user.password, user.status)

@users_router.get("/", response_model=list[UserOut])
async def list_users():
    return await dispatch("user", "get_all")

@users_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user = await dispatch("user", "get_by_id", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.get("/{user_id}/username")
async def get_current_username(user_id: int):
    usernames = await dispatch("username", "get_all", user_id)
    current = next((u for u in reversed(usernames) if u.current), None) if usernames else None
    return {"user_id": user_id, "username": current.user_status if current else None}


@users_router.put("/{user_id}/status", response_model=UserOut)
async def update_status(user_id: int, new_status: str):
    updated = await dispatch("user", "update_status", user_id, new_status)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@users_router.put("/{user_id}/profile_pic", response_model=UserOut)
async def update_profile_pic(user_id: int, pic_url: str):
    updated = await dispatch("user", "update_profile_pic", user_id, pic_url)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@users_router.delete("/{user_id}")
async def delete_user(user_id: int):
    deleted = await dispatch("user", "delete", user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

@users_router.put("/{user_id}/password", response_model=UserOut)
async def change_password(user_id: int, old_password: str, new_password: str):
    updated = await dispatch("user", "change_password", user_id, old_password, new_password)
    if updated is None:  
        raise HTTPException(status_code=404, detail="User not found")
    if updated is False:  
        raise HTTPException(status_code=400, detail="Invalid old password")
    return updated


@users_router.post("/{user_id}/password/log", response_model=PasswordChangeOut)
async def log_password_change(user_id: int, old_password: str, new_password: str):
    return await dispatch("password_change", "log", user_id, old_password, new_password)

@users_router.get("/{user_id}/password/history", response_model=list[PasswordChangeOut])
async def get_password_changes(user_id: int):
    return await dispatch("password_change", "get_all", user_id)

@users_router.put("/{user_id}/username", response_model=UsernameOut)
async def change_username(user_id: int, new_username: str):
    existing = await dispatch("username", "get_by_status", new_username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    updated = await dispatch("username", "change", user_id, new_username)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
