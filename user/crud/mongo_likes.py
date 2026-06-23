from fastapi import HTTPException

from settings.mongodb import ensure_like_indexes, get_mongo_db, utc_now

try:
    from pymongo.errors import DuplicateKeyError, PyMongoError
except ImportError:  # pragma: no cover - dependency is installed with motor.
    DuplicateKeyError = Exception
    PyMongoError = Exception


def serialize_mongo_doc(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["_id"] = str(doc["_id"])
    return doc


async def record_post_like(post_id: int, post_owner_user_id: int | None, liked_by_user_id: int):
    await ensure_like_indexes()
    db = get_mongo_db()
    document = {
        "content_type": "post",
        "post_id": post_id,
        "content_owner_user_id": post_owner_user_id,
        "liked_by_user_id": liked_by_user_id,
        "liked_at": utc_now(),
    }
    try:
        result = await db.post_likes.update_one(
            {"post_id": post_id, "liked_by_user_id": liked_by_user_id},
            {"$setOnInsert": document},
            upsert=True,
        )
        if result.upserted_id:
            document["_id"] = str(result.upserted_id)
            return document
        existing = await db.post_likes.find_one({"post_id": post_id, "liked_by_user_id": liked_by_user_id})
        return serialize_mongo_doc(existing)
    except DuplicateKeyError:
        existing = await db.post_likes.find_one({"post_id": post_id, "liked_by_user_id": liked_by_user_id})
        return serialize_mongo_doc(existing)
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB post like write failed: {exc}") from exc


async def remove_post_like(post_id: int, liked_by_user_id: int):
    await ensure_like_indexes()
    db = get_mongo_db()
    try:
        result = await db.post_likes.delete_one({"post_id": post_id, "liked_by_user_id": liked_by_user_id})
        return result.deleted_count > 0
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB post like delete failed: {exc}") from exc


async def get_post_like_details(post_id: int):
    await ensure_like_indexes()
    db = get_mongo_db()
    try:
        cursor = db.post_likes.find({"post_id": post_id}).sort("liked_at", -1)
        return [serialize_mongo_doc(doc) async for doc in cursor]
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB post like read failed: {exc}") from exc


async def record_reel_like(reel_id: int, reel_owner_user_id: int | None, liked_by_user_id: int):
    await ensure_like_indexes()
    db = get_mongo_db()
    document = {
        "content_type": "reel",
        "reel_id": reel_id,
        "content_owner_user_id": reel_owner_user_id,
        "liked_by_user_id": liked_by_user_id,
        "liked_at": utc_now(),
    }
    try:
        result = await db.reel_likes.update_one(
            {"reel_id": reel_id, "liked_by_user_id": liked_by_user_id},
            {"$setOnInsert": document},
            upsert=True,
        )
        if result.upserted_id:
            document["_id"] = str(result.upserted_id)
            return document
        existing = await db.reel_likes.find_one({"reel_id": reel_id, "liked_by_user_id": liked_by_user_id})
        return serialize_mongo_doc(existing)
    except DuplicateKeyError:
        existing = await db.reel_likes.find_one({"reel_id": reel_id, "liked_by_user_id": liked_by_user_id})
        return serialize_mongo_doc(existing)
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB reel like write failed: {exc}") from exc


async def remove_reel_like(reel_id: int, liked_by_user_id: int):
    await ensure_like_indexes()
    db = get_mongo_db()
    try:
        result = await db.reel_likes.delete_one({"reel_id": reel_id, "liked_by_user_id": liked_by_user_id})
        return result.deleted_count > 0
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB reel like delete failed: {exc}") from exc


async def get_reel_like_details(reel_id: int):
    await ensure_like_indexes()
    db = get_mongo_db()
    try:
        cursor = db.reel_likes.find({"reel_id": reel_id}).sort("liked_at", -1)
        return [serialize_mongo_doc(doc) async for doc in cursor]
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB reel like read failed: {exc}") from exc
