from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from settings.database import get_session
from models import AdminPrivacyOverride, Privacy


async def admin_override_user_privacy(user_id: int, new_status: str, reason: str = None):
    try:
        async with get_session() as session:
            # Update the user's current privacy record
            new_priv = Privacy(user_id=user_id, priv_status=new_status, current=True)
            session.add(new_priv)
            # Log the override
            override = AdminPrivacyOverride(
                user_id=user_id,
                policy_value=new_status,
                reason=reason
            )
            session.add(override)
            await session.commit()
            await session.refresh(override)
            return override
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_get_all_privacy_overrides():
    try:
        async with get_session() as session:
            result = await session.execute(
                select(AdminPrivacyOverride).where(AdminPrivacyOverride.user_id.isnot(None))
            )
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_create_global_privacy_policy(policy_name: str, policy_value: str):
    try:
        async with get_session() as session:
            policy = AdminPrivacyOverride(
                user_id=None,
                policy_name=policy_name,
                policy_value=policy_value
            )
            session.add(policy)
            await session.commit()
            await session.refresh(policy)
            return policy
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def admin_get_global_privacy_policies():
    try:
        async with get_session() as session:
            result = await session.execute(
                select(AdminPrivacyOverride).where(AdminPrivacyOverride.user_id.is_(None))
            )
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
