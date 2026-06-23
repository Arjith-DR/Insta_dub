from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import Follower


async def follow_user(follower_id: int, following_id: int):
    if follower_id == following_id:
        raise ValueError("Users cannot follow themselves")
    async with get_session() as session:
        try:
            follower = Follower(follower_id=follower_id, following_id=following_id)
            session.add(follower)
            await session.commit()
            return follower
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_followers(user_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(Follower).where(Follower.following_id == user_id))
            return result.scalars().all()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_following(user_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(Follower).where(Follower.follower_id == user_id))
            return result.scalars().all()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def unfollow_user(follower_id: int, following_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(Follower).where(Follower.follower_id == follower_id, Follower.following_id == following_id)
            )
            follow = result.scalars().first()
            if follow:
                await session.delete(follow)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
