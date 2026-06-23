from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from core.schemas import ContentCreate, ContentOut


content_router = APIRouter(prefix="/content", tags=["content"])


@content_router.post("/", response_model=ContentOut)
async def create_content(content: ContentCreate):
    return await dispatch("content", "create", content.user_id, content.type, content.status)


@content_router.get("/{user_id}", response_model=list[ContentOut])
async def get_content(user_id: int):
    return await dispatch("content", "get_all", user_id)


@content_router.put("/{content_id}", response_model=ContentOut)
async def update_content(content_id: int, new_status: str):
    updated = await dispatch("content", "update", content_id, new_status)
    if not updated:
        raise HTTPException(status_code=404, detail="Content not found")
    return updated


@content_router.delete("/{content_id}")
async def delete_content(content_id: int):
    deleted = await dispatch("content", "delete", content_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"detail": "Content deleted"}
