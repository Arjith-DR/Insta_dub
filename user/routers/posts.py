from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from user.schemas import PostCreate, PostOut, PostCommentCreate, PostCommentOut, PostMediaCreate, PostMediaOut,PostLikeOut
from user.crud.pg_likes import record_post_like, remove_post_like, get_post_like_details

posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.post("/", response_model=PostOut)
async def create_post(post: PostCreate):
    return await dispatch("post", "create", post.user_id, post.caption, post.status)

@posts_router.get("/", response_model=list[PostOut])
async def list_posts(requester_id: int):
    return await dispatch("post", "get_all", requester_id)

@posts_router.get("/by_user/{user_id}", response_model=list[PostOut])
async def get_user_posts(user_id: int):
    return await dispatch("post", "get_by_user", user_id)

@posts_router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, new_caption: str):
    updated = await dispatch("post", "update", post_id, new_caption)
    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated

@posts_router.delete("/{post_id}")
async def delete_post(post_id: int):
    deleted = await dispatch("post", "delete", post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}

@posts_router.post("/{post_id}/comments", response_model=PostCommentOut)
async def add_post_comment(post_id: int, comment: PostCommentCreate):
    return await dispatch("post", "comment", post_id, comment.user_id, comment.text)

@posts_router.delete("/comments/{comment_id}")
async def delete_post_comment(comment_id: int):
    deleted = await dispatch("post", "delete_comment", comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"detail": "Comment deleted"}

@posts_router.post("/{post_id}/likes", response_model=PostLikeOut)
async def like_post(post_id: int, user_id: int, owner_id: int = 0):
    return await record_post_like(post_id, owner_id, user_id)

@posts_router.get("/{post_id}/likes/details", response_model=list[PostLikeOut])
async def list_post_like_details(post_id: int):
    return await get_post_like_details(post_id)

@posts_router.delete("/{post_id}/likes/{user_id}")
async def unlike_post(post_id: int, user_id: int):
    deleted = await remove_post_like(post_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"deleted": True}

@posts_router.post("/{post_id}/media", response_model=PostMediaOut)
async def add_post_media(post_id: int, media: PostMediaCreate):
    return await dispatch("post", "add_media", post_id, media.media_url, media.media_type, media.order_index)

@posts_router.delete("/media/{media_id}")
async def remove_post_media(media_id: int):
    deleted = await dispatch("post", "remove_media", media_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"detail": "Media removed"}
