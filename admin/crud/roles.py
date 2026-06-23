from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import Role, UserRole


async def create_role(role_name: str, description: str = None):
    try:
        async with get_session() as session:
            new_role = Role(role_name=role_name, description=description)
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)
            return new_role
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_roles():
    try:
        async with get_session() as session:
            result = await session.execute(select(Role))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_role_by_id(role_id: int):
    try:
        async with get_session() as session:
            return await session.get(Role, role_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def assign_role_to_user(user_id: int, role_id: int):
    try:
        async with get_session() as session:
            user_role = UserRole(user_id=user_id, role_id=role_id)
            session.add(user_role)
            await session.commit()
            await session.refresh(user_role)
            return user_role
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def remove_role_from_user(user_id: int, role_id: int):
    try:
        async with get_session() as session:
            result = await session.execute(
                select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
            )
            user_role = result.scalars().first()
            if not user_role:
                return False
            await session.delete(user_role)
            await session.commit()
            return True
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_user_roles(user_id: int):
    try:
        async with get_session() as session:
            result = await session.execute(
                select(Role)
                .join(UserRole, UserRole.role_id == Role.role_id)
                .where(UserRole.user_id == user_id)
            )
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
