from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, delete
from fastapi import HTTPException
from settings.database import get_session
from models import Reel, ReelComment, Privacy, Follower
from user.crud.mongo_likes import remove_reel_likes_for_reel


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
            raise HTTPException(status_code=404, detail="Reel not found")
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_reel(reel_id: int):
    async with get_session() as session:
        try:
            reel = await session.get(Reel, reel_id)
            if reel:
                await remove_reel_likes_for_reel(reel_id)
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



