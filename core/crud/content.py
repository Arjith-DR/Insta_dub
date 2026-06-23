from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import Content



async def create_content(user_id: int, type: str, status="active"):
    try:
        async with get_session() as session:
            new_content = Content(user_id=user_id, type=type, status=status)
            session.add(new_content)
            await session.commit()
            await session.refresh(new_content)
            return new_content
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_content(user_id: int):
    try:
        async with get_session() as session:
            result = await session.execute(select(Content).where(Content.user_id == user_id))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_content_by_id(content_id: int):
    try:
        async with get_session() as session:
            return await session.get(Content, content_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def update_content(content_id: int, new_status: str):
    try:
        async with get_session() as session:
            content = await session.get(Content, content_id)
            if content:
                content.status = new_status
                await session.commit()
                return content
            return None
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_content(content_id: int):
    try:
        async with get_session() as session:
            content = await session.get(Content, content_id)
            if content:
                await session.delete(content)
                await session.commit()
                return True
            return False
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
