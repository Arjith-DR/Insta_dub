"""PostgreSQL-backed likes CRUD — replaces the MongoDB mongo_likes module."""
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from settings.database import get_session
from models import PostLike, ReelLike


# ─── Post Likes ───────────────────────────────────────────────────────────────

async def record_post_like(post_id: int, post_owner_user_id: int, liked_by_user_id: int):
    async with get_session() as session:
        try:
            like = PostLike(
                post_id=post_id,
                liked_by_user_id=liked_by_user_id,
                content_owner_user_id=post_owner_user_id,
            )
            session.add(like)
            await session.commit()
            await session.refresh(like)
            return {
                "content_type": "post",
                "post_id": like.post_id,
                "content_owner_user_id": like.content_owner_user_id,
                "liked_by_user_id": like.liked_by_user_id,
                "liked_at": like.liked_at,
            }
        except IntegrityError:
            await session.rollback()
            # Already liked — return existing record
            result = await session.execute(
                select(PostLike).where(
                    PostLike.post_id == post_id,
                    PostLike.liked_by_user_id == liked_by_user_id,
                )
            )
            existing = result.scalars().first()
            if existing:
                return {
                    "content_type": "post",
                    "post_id": existing.post_id,
                    "content_owner_user_id": existing.content_owner_user_id,
                    "liked_by_user_id": existing.liked_by_user_id,
                    "liked_at": existing.liked_at,
                }
            return {"content_type": "post", "post_id": post_id, "liked_by_user_id": liked_by_user_id}
        except SQLAlchemyError as exc:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Post like write failed: {exc}") from exc


async def remove_post_like(post_id: int, liked_by_user_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(PostLike).where(
                    PostLike.post_id == post_id,
                    PostLike.liked_by_user_id == liked_by_user_id,
                )
            )
            like = result.scalars().first()
            if like:
                await session.delete(like)
                await session.commit()
                return True
            return False
        except SQLAlchemyError as exc:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Post like delete failed: {exc}") from exc


async def get_post_like_details(post_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(PostLike).where(PostLike.post_id == post_id).order_by(PostLike.liked_at.desc())
            )
            likes = result.scalars().all()
            return [
                {
                    "content_type": "post",
                    "post_id": l.post_id,
                    "content_owner_user_id": l.content_owner_user_id,
                    "liked_by_user_id": l.liked_by_user_id,
                    "liked_at": l.liked_at,
                }
                for l in likes
            ]
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=500, detail=f"Post like read failed: {exc}") from exc


async def count_post_likes(post_id: int) -> int:
    async with get_session() as session:
        try:
            from sqlalchemy import func
            result = await session.execute(
                select(func.count()).select_from(PostLike).where(PostLike.post_id == post_id)
            )
            return result.scalar() or 0
        except SQLAlchemyError:
            return 0


# ─── Reel Likes ───────────────────────────────────────────────────────────────

async def record_reel_like(reel_id: int, reel_owner_user_id: int, liked_by_user_id: int):
    async with get_session() as session:
        try:
            like = ReelLike(
                reel_id=reel_id,
                liked_by_user_id=liked_by_user_id,
                content_owner_user_id=reel_owner_user_id,
            )
            session.add(like)
            await session.commit()
            await session.refresh(like)
            return {
                "content_type": "reel",
                "reel_id": like.reel_id,
                "content_owner_user_id": like.content_owner_user_id,
                "liked_by_user_id": like.liked_by_user_id,
                "liked_at": like.liked_at,
            }
        except IntegrityError:
            await session.rollback()
            result = await session.execute(
                select(ReelLike).where(
                    ReelLike.reel_id == reel_id,
                    ReelLike.liked_by_user_id == liked_by_user_id,
                )
            )
            existing = result.scalars().first()
            if existing:
                return {
                    "content_type": "reel",
                    "reel_id": existing.reel_id,
                    "content_owner_user_id": existing.content_owner_user_id,
                    "liked_by_user_id": existing.liked_by_user_id,
                    "liked_at": existing.liked_at,
                }
            return {"content_type": "reel", "reel_id": reel_id, "liked_by_user_id": liked_by_user_id}
        except SQLAlchemyError as exc:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Reel like write failed: {exc}") from exc


async def remove_reel_like(reel_id: int, liked_by_user_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(ReelLike).where(
                    ReelLike.reel_id == reel_id,
                    ReelLike.liked_by_user_id == liked_by_user_id,
                )
            )
            like = result.scalars().first()
            if like:
                await session.delete(like)
                await session.commit()
                return True
            return False
        except SQLAlchemyError as exc:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Reel like delete failed: {exc}") from exc


async def get_reel_like_details(reel_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(ReelLike).where(ReelLike.reel_id == reel_id).order_by(ReelLike.liked_at.desc())
            )
            likes = result.scalars().all()
            return [
                {
                    "content_type": "reel",
                    "reel_id": l.reel_id,
                    "content_owner_user_id": l.content_owner_user_id,
                    "liked_by_user_id": l.liked_by_user_id,
                    "liked_at": l.liked_at,
                }
                for l in likes
            ]
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=500, detail=f"Reel like read failed: {exc}") from exc


async def count_reel_likes(reel_id: int) -> int:
    async with get_session() as session:
        try:
            from sqlalchemy import func
            result = await session.execute(
                select(func.count()).select_from(ReelLike).where(ReelLike.reel_id == reel_id)
            )
            return result.scalar() or 0
        except SQLAlchemyError:
            return 0


# Stubs kept for compatibility with base_crud ACTION_MAP
async def remove_post_likes_for_post(post_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(PostLike).where(PostLike.post_id == post_id))
            likes = result.scalars().all()
            for like in likes:
                await session.delete(like)
            await session.commit()
            return len(likes)
        except SQLAlchemyError as exc:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Post likes batch delete failed: {exc}") from exc


async def remove_reel_likes_for_reel(reel_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(ReelLike).where(ReelLike.reel_id == reel_id))
            likes = result.scalars().all()
            for like in likes:
                await session.delete(like)
            await session.commit()
            return len(likes)
        except SQLAlchemyError as exc:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Reel likes batch delete failed: {exc}") from exc
