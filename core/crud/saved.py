from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import SavedCategory, SavedItem



async def create_saved_category(user_id: int, name: str):
    try:
        async with get_session() as session:
            new_category = SavedCategory(user_id=user_id, name=name)
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_saved_categories(user_id: int):
    try:
        async with get_session() as session:
            result = await session.execute(select(SavedCategory).where(SavedCategory.user_id == user_id))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def add_saved_item(user_id: int, content_id: int, category_id: int = None):
    try:
        async with get_session() as session:
            new_item = SavedItem(user_id=user_id, content_id=content_id, category_id=category_id, is_saved=True)
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            return new_item
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def remove_saved_item(saved_id: int):
    try:
        async with get_session() as session:
            item = await session.get(SavedItem, saved_id)
            if item:
                await session.delete(item)
                await session.commit()
                return True
            return False
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
