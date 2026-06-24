from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from user.schemas import ReelCreate, ReelOut, ReelCommentCreate, ReelCommentOut, ReelLikeOut
from user.crud.mongo_likes import record_reel_like, remove_reel_like, get_reel_like_details

reels_router = APIRouter(prefix="/reels", tags=["reels"])


@reels_router.post("/", response_model=ReelOut)
async def create_reel(reel: ReelCreate):
    return await dispatch("reel", "create", reel.user_id, reel.video_url, reel.caption, reel.status)

@reels_router.get("/", response_model=list[ReelOut])
async def list_reels(requester_id: int):
    return await dispatch("reel", "get_all", requester_id)

@reels_router.put("/{reel_id}", response_model=ReelOut)
async def update_reel(reel_id: int, new_caption: str):
    updated = await dispatch("reel", "update", reel_id, new_caption)
    if not updated:
        raise HTTPException(status_code=404, detail="Reel not found")
    return updated

@reels_router.delete("/{reel_id}")
async def delete_reel(reel_id: int):
    deleted = await dispatch("reel", "delete", reel_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reel not found")
    return {"detail": "Reel deleted"}

@reels_router.post("/{reel_id}/comments", response_model=ReelCommentOut)
async def add_reel_comment(reel_id: int, comment: ReelCommentCreate):
    return await dispatch("reel", "comment", reel_id, comment.user_id, comment.text)

@reels_router.delete("/comments/{comment_id}")
async def delete_reel_comment(comment_id: int):
    deleted = await dispatch("reel", "delete_comment", comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"detail": "Comment deleted"}

async def like_reel(reel_id: int, user_id: int, owner_id: int):
    return await record_reel_like(reel_id, owner_id, user_id)

@reels_router.get("/{reel_id}/likes/details", response_model=list[ReelLikeOut])
async def list_reel_like_details(reel_id: int):
    return await get_reel_like_details(reel_id)

@reels_router.delete("/{reel_id}/likes/{user_id}")
async def unlike_reel(reel_id: int, user_id: int):
    deleted = await remove_reel_like(reel_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"deleted": True}
