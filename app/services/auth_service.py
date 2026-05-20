import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User, OAuthAccount, UserSettings, UserProgress
from app.core.security import hash_password, verify_password


async def register_user(db: AsyncSession, email: str, username: str, password: str) -> User:
    if await _email_exists(db, email):
        raise HTTPException(status_code=409, detail="Email already registered")
    if await _username_exists(db, username):
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(email=email, username=username, password_hash=hash_password(password))
    db.add(user)
    await db.flush()
    await _create_user_defaults(db, user.id)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, email: str, password: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


async def get_or_create_oauth_user(
    db: AsyncSession,
    provider: str,
    provider_user_id: str,
    email: str,
    username: str,
) -> User:
    result = await db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id,
        )
    )
    oauth_account = result.scalar_one_or_none()

    if oauth_account:
        result = await db.execute(select(User).where(User.id == oauth_account.user_id))
        return result.scalar_one()

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        safe_username = await _unique_username(db, username)
        user = User(email=email, username=safe_username)
        db.add(user)
        await db.flush()
        await _create_user_defaults(db, user.id)

    db.add(OAuthAccount(user_id=user.id, provider=provider, provider_user_id=provider_user_id))
    await db.commit()
    await db.refresh(user)
    return user


async def _email_exists(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None


async def _username_exists(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none() is not None


async def _unique_username(db: AsyncSession, base: str) -> str:
    candidate = base.replace(" ", "_").lower()[:30]
    counter = 0
    while await _username_exists(db, candidate):
        counter += 1
        candidate = f"{base[:27]}_{counter}"
    return candidate


async def _create_user_defaults(db: AsyncSession, user_id: uuid.UUID) -> None:
    db.add(UserSettings(user_id=user_id))
    db.add(UserProgress(user_id=user_id))
