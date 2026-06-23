from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, delete
from fastapi import HTTPException
from settings.database import get_session
from models import Reel, ReelComment, ReelLike, Privacy, Follower
from user.crud.mongo_likes import record_reel_like, remove_reel_like, get_reel_like_details


async def create_reel(user_id: int, video_url: str, caption: str, status="active"):
    async with get_session() as session:
        try:
            new_reel = Reel(user_id=user_id, video_url=video_url, caption=caption, status=status)
            session.add(new_reel)
            await session.commit()
            await session.refresh(new_reel)
            return new_reel
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_reels(requester_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(Reel))
            reels = result.scalars().all()
            visible_reels = []
            for reel in reels:
                priv_result = await session.execute(
                    select(Privacy).where(Privacy.user_id == reel.user_id, Privacy.current == True)
                )
                privacy = priv_result.scalars().first()
                if not privacy or privacy.priv_status == "public":
                    visible_reels.append(reel)
                elif reel.user_id == requester_id:
                    visible_reels.append(reel)
                else:
                    follow_result = await session.execute(
                        select(Follower).where(
                            and_(Follower.follower_id == requester_id, Follower.following_id == reel.user_id)
                        )
                    )
                    if follow_result.scalars().first():
                        visible_reels.append(reel)
            return visible_reels
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def update_reel(reel_id: int, new_caption: str):
    async with get_session() as session:
        try:
            reel = await session.get(Reel, reel_id)
            if reel:
                reel.caption = new_caption
                await session.commit()
                return reel
            return None
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_reel(reel_id: int):
    async with get_session() as session:
        try:
            reel = await session.get(Reel, reel_id)
            if reel:
                await session.execute(delete(ReelLike).where(ReelLike.reel_id == reel_id))
                await session.execute(delete(ReelComment).where(ReelComment.reel_id == reel_id))
                await session.delete(reel)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def add_reel_comment(reel_id: int, user_id: int, text: str):
    async with get_session() as session:
        try:
            new_comment = ReelComment(reel_id=reel_id, user_id=user_id, text=text)
            session.add(new_comment)
            await session.commit()
            await session.refresh(new_comment)
            return new_comment
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_reel_comment(comment_id: int):
    async with get_session() as session:
        try:
            comment = await session.get(ReelComment, comment_id)
            if comment:
                await session.delete(comment)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def like_reel(reel_id: int, user_id: int):
    async with get_session() as session:
        try:
            reel = await session.get(Reel, reel_id)
            if not reel:
                raise HTTPException(status_code=404, detail="Reel not found")

            existing_result = await session.execute(
                select(ReelLike).where(ReelLike.reel_id == reel_id, ReelLike.user_id == user_id)
            )
            existing_like = existing_result.scalars().first()
            if existing_like:
                try:
                    await record_reel_like(reel_id, reel.user_id, user_id)
                except Exception:
                    pass
                return existing_like

            new_like = ReelLike(reel_id=reel_id, user_id=user_id, is_liked=True)
            session.add(new_like)
            await session.commit()
            await session.refresh(new_like)
            try:
                await record_reel_like(reel_id, reel.user_id, user_id)
            except Exception:
                pass
            return new_like
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))


async def unlike_reel(reel_id: int, user_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(ReelLike).where(ReelLike.reel_id == reel_id, ReelLike.user_id == user_id)
            )
            like = result.scalars().first()
            mongo_deleted = False
            try:
                mongo_deleted = await remove_reel_like(reel_id, user_id)
            except Exception:
                pass
            if like:
                await session.delete(like)
                await session.commit()
                return True
            return mongo_deleted
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))


async def get_reel_likes(reel_id: int):
    return await get_reel_like_details(reel_id)
