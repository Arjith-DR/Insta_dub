from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import Privacy, PasswordChange



async def update_privacy(user_id: int, new_status: str):
    try:
        async with get_session() as session:
            new_priv = Privacy(user_id=user_id, priv_status=new_status, current=True)
            session.add(new_priv)
            await session.commit()
            await session.refresh(new_priv)
            return new_priv
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_privacies(user_id: int):
    try:
        async with get_session() as session:
            result = await session.execute(select(Privacy).where(Privacy.user_id == user_id))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def log_password_change(user_id: int, old_password: str, new_password: str):
    try:
        async with get_session() as session:
            change = PasswordChange(user_id=user_id, old_password=old_password, new_password=new_password)
            session.add(change)
            await session.commit()
            await session.refresh(change)
            return change
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_password_changes(user_id: int):
    try:
        async with get_session() as session:
            result = await session.execute(select(PasswordChange).where(PasswordChange.user_id == user_id))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
