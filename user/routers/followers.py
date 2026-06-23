from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from user.schemas import FollowerOut

followers_router = APIRouter(prefix="/followers", tags=["followers"])


@followers_router.post("/", response_model=FollowerOut)
async def follow_user(follower_id: int, following_id: int):
    if follower_id == following_id:
        raise HTTPException(status_code=400, detail="Users cannot follow themselves")
    return await dispatch("follower", "follow", follower_id, following_id)


@followers_router.get("/{user_id}", response_model=list[FollowerOut])
async def get_followers(user_id: int):
    return await dispatch("follower", "get_followers", user_id)

@followers_router.get("/following/{user_id}", response_model=list[FollowerOut])
async def get_following(user_id: int):
    return await dispatch("follower", "get_following", user_id)

@followers_router.delete("/{follower_id}/{following_id}")
async def unfollow_user(follower_id: int, following_id: int):
    deleted = await dispatch("follower", "unfollow", follower_id, following_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    return {"detail": "Unfollowed successfully"}
