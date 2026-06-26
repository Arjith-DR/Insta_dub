from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from user.schemas import BioCreate, BioOut

bios_router = APIRouter(prefix="/bios", tags=["bios"])


@bios_router.post("/", response_model=BioOut)
async def create_bio(bio: BioCreate):
    return await dispatch("bio", "create", bio.user_id, bio.text, bio.current)

@bios_router.get("/{user_id}")
async def get_bio(user_id: int):
    bios = await dispatch("bio", "get_all")
    for b in bios:
        if b.user_id == user_id and b.current:
            return b
    return {"user_id": user_id, "b_txt": "", "current": True}


@bios_router.put("/{bio_id}", response_model=BioOut)
async def update_bio(bio_id: int, new_text: str):
    updated = await dispatch("bio", "update", bio_id, new_text)
    if not updated:
        raise HTTPException(status_code=404, detail="Bio not found")
    return updated

@bios_router.delete("/{bio_id}")
async def delete_bio(bio_id: int):
    deleted = await dispatch("bio", "delete", bio_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bio not found")
    return {"detail": "Bio deleted"}
