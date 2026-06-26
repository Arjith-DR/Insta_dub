from fastapi import APIRouter
from pydantic import BaseModel
from base_crud import dispatch

privacy_router = APIRouter(prefix="/privacy", tags=["privacy"])

class PrivacyOut(BaseModel):
    user_id: int
    priv_status: str

    class Config:
        from_attributes = True

@privacy_router.put("/{user_id}", response_model=PrivacyOut)
async def update_privacy(user_id: int, priv_status: str):
    return await dispatch("privacy", "update", user_id, priv_status)

@privacy_router.get("/{user_id}", response_model=PrivacyOut)
async def get_privacy(user_id: int):
    # we don't have a specific get_privacy for one user in ACTION_MAP, 
    # but we can get all and filter or just let frontend handle state
    # Wait, get_privacies gets all privacies. Let's filter here.
    privacies = await dispatch("privacy", "get_all")
    for p in privacies:
        if p.user_id == user_id and p.current:
            return p
    return {"user_id": user_id, "priv_status": "public"}
