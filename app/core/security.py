from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "type": "access"},
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "type": "refresh"},
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def set_auth_cookies(response, access_token: str, refresh_token: str) -> None:
    opts = dict(httponly=True, secure=True, samesite="none")
    response.set_cookie(
        "access_token", access_token,
        max_age=settings.access_token_expire_minutes * 60, **opts
    )
    response.set_cookie(
        "refresh_token", refresh_token,
        max_age=settings.refresh_token_expire_days * 86400, **opts
    )


def clear_auth_cookies(response) -> None:
    opts = dict(httponly=True, secure=True, samesite="none")
    response.delete_cookie("access_token", **opts)
    response.delete_cookie("refresh_token", **opts)
