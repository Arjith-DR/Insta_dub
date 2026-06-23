from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from core.schemas import LoginRequest, Token
from core.security import verify_password, create_access_token
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
        return Token(access_token=access_token)
