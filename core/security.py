import hashlib
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.future import select
from settings.config import settings
from settings.database import Base, engine, get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "token_type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _is_missing_refresh_tokens_table(error: Exception) -> bool:
    message = str(error).lower()
    return "refresh_tokens" in message and ("does not exist" in message or "undefinedtable" in message)


async def ensure_refresh_token_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def store_refresh_token(user_id: int, refresh_token: str) -> None:
    from models import RefreshToken

    async with get_session() as session:
        token_hash = _hash_token(refresh_token)
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        try:
            session.add(
                RefreshToken(
                    user_id=user_id,
                    token_hash=token_hash,
                    expires_at=expires_at,
                    revoked=False,
                )
            )
            await session.commit()
        except ProgrammingError as exc:
            if not _is_missing_refresh_tokens_table(exc):
                raise
            if hasattr(session, "rollback"):
                await session.rollback()
            try:
                await ensure_refresh_token_table()
            except Exception:
                return
            try:
                async with get_session() as retry_session:
                    retry_session.add(
                        RefreshToken(
                            user_id=user_id,
                            token_hash=token_hash,
                            expires_at=expires_at,
                            revoked=False,
                        )
                    )
                    await retry_session.commit()
            except Exception:
                return


async def verify_refresh_token(token: str):
    from models import RefreshToken

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("token_type") != "refresh":
            return None
        subject = payload.get("sub")
        if subject is None:
            return None
        user_id = int(subject)
    except (JWTError, ValueError, TypeError):
        return None

    async with get_session() as session:
        try:
            token_hash = _hash_token(token)
            result = await session.execute(
                select(RefreshToken).where(
                    RefreshToken.user_id == user_id,
                    RefreshToken.token_hash == token_hash,
                    RefreshToken.revoked.is_(False),
                    RefreshToken.expires_at > datetime.now(timezone.utc),
                )
            )
            stored_token = result.scalars().first()
            if stored_token is None:
                return None
            return user_id
        except ProgrammingError:
            return None


async def is_admin_user(user) -> bool:
    from models import Role, UserRole

    if getattr(user, "role_id", None) is not None and int(user.role_id) == 2:
        return True

    async with get_session() as session:
        role_result = await session.execute(select(Role.role_name).where(Role.role_id == getattr(user, "role_id", None)))
        role_name = role_result.scalars().first()
        if role_name and role_name.lower() == "admin":
            return True

        result = await session.execute(
            select(Role.role_name)
            .join(UserRole, UserRole.role_id == Role.role_id)
            .where(UserRole.user_id == user.user_id)
        )
        role_names = [row[0] for row in result.all()]
        return any(name and name.lower() == "admin" for name in role_names)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("token_type") != "access":
            raise credentials_exception
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    from models import User
    async with get_session() as session:
        user = await session.get(User, user_id)
        if user is None:
            raise credentials_exception
        return user


async def get_current_admin_user(current_user=Depends(get_current_user)):
    if not await is_admin_user(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
