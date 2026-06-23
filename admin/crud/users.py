from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import User
from core.security import hash_password


async def admin_list_users():
    try:
        async with get_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_hard_delete_user(user_id: int):
    try:
        async with get_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return None
            await session.delete(user)
            await session.commit()
            return True
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_activate_user(user_id: int):
    try:
        async with get_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return None
            user.status = "active"
            await session.commit()
            return user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_deactivate_user(user_id: int):
    try:
        async with get_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return None
            user.status = "inactive"
            await session.commit()
            return user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_reset_password(user_id: int, new_password: str):
    try:
        async with get_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return None
            user.password = hash_password(new_password)
            await session.commit()
            return user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
