from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import User, Username, PasswordChange
from core.security import hash_password, verify_password


async def create_user(role_id, email, password, status="active"):
    async with get_session() as session:
        try:
            hashed_pw = hash_password(password)
            new_user = User(role_id=role_id, email=email, password=hashed_pw, status=status)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_users():
    async with get_session() as session:
        try:
            result = await session.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_user_by_id(user_id: int):
    async with get_session() as session:
        try:
            return await session.get(User, user_id)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def update_user_status(user_id: int, new_status: str):
    async with get_session() as session:
        try:
            user = await session.get(User, user_id)
            if user:
                user.status = new_status
                await session.commit()
                return user
            return None
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_user(user_id: int):
    async with get_session() as session:
        try:
            user = await session.get(User, user_id)
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def change_password(user_id: int, old_password: str, new_password: str):
    async with get_session() as session:
        try:
            user = await session.get(User, user_id)
            if user and verify_password(old_password, user.password):
                hashed_pw = hash_password(new_password)
                user.password = hashed_pw
                change = PasswordChange(user_id=user_id, old_password=user.password, new_password=hashed_pw)
                session.add(change)
                await session.commit()
                return user
            return None
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def change_username(user_id: int, new_username: str):
    async with get_session() as session:
        try:
            new_name = Username(user_id=user_id, user_status=new_username, current=True)
            session.add(new_name)
            await session.commit()
            await session.refresh(new_name)
            return new_name
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_usernames(user_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(Username).where(Username.user_id == user_id))
            return result.scalars().all()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_username_by_status(username: str):
    async with get_session() as session:
        try:
            result = await session.execute(select(Username).where(Username.user_status == username))
            return result.scalars().first()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
