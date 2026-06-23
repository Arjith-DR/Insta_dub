from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import Bio


async def create_bio(user_id: int, text: str, current=True):
    async with get_session() as session:
        try:
            new_bio = Bio(user_id=user_id, b_txt=text, current=current)
            session.add(new_bio)
            await session.commit()
            await session.refresh(new_bio)
            return new_bio
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def update_bio(bio_id: int, new_text: str):
    async with get_session() as session:
        try:
            bio = await session.get(Bio, bio_id)
            if bio:
                bio.b_txt = new_text
                await session.commit()
                return bio
            return None
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_bio(bio_id: int):
    async with get_session() as session:
        try:
            bio = await session.get(Bio, bio_id)
            if bio:
                await session.delete(bio)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
