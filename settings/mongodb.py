from datetime import datetime, timezone

from fastapi import HTTPException

from settings.config import settings

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except ImportError:  
    AsyncIOMotorClient = None


_client = None
_indexes_ready = False


def get_mongo_db():
    global _client
    if AsyncIOMotorClient is None:
        raise HTTPException(
            status_code=500,
            detail="MongoDB support requires motor. Run: pip install -r requirements.txt",
        )
    if _client is None:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT_MS,
        )
    return _client[settings.MONGODB_DB_NAME]


async def ensure_like_indexes():
    global _indexes_ready
    if _indexes_ready:
        return

    db = get_mongo_db()
    await db.post_likes.create_index(
        [("post_id", 1), ("liked_by_user_id", 1)],
        unique=True,
        name="unique_post_like",
    )
    await db.reel_likes.create_index(
        [("reel_id", 1), ("liked_by_user_id", 1)],
        unique=True,
        name="unique_reel_like",
    )
    await db.post_likes.create_index("liked_at")
    await db.reel_likes.create_index("liked_at")
    _indexes_ready = True


def utc_now():
    return datetime.now(timezone.utc)