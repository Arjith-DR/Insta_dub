from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from core.schemas import LoginRequest, RefreshTokenRequest, Token
from core.security import verify_password, create_access_token, create_refresh_token, store_refresh_token, verify_refresh_token
from settings.database import get_session
from models import User


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    async with get_session() as session:
        result = await session.execute(select(User).where(User.email == request.email))
        user = result.scalars().first()
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(data={"sub": user.user_id})
        refresh_token = create_refresh_token(data={"sub": user.user_id})
        await store_refresh_token(user.user_id, refresh_token)
        return Token(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model=Token)
async def refresh(request: RefreshTokenRequest):
    user_id = await verify_refresh_token(request.refresh_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})
    await store_refresh_token(user_id, refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)
