from typing import Optional
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import (
    create_access_token, create_refresh_token, decode_token,
    set_auth_cookies, clear_auth_cookies,
)
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from app.services.auth_service import login_user, register_user, get_or_create_oauth_user

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
oauth.register(
    name="github",
    client_id=settings.github_client_id,
    client_secret=settings.github_client_secret,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

router = APIRouter(prefix="/auth", tags=["auth"])


async def _oauth_redirect(db: AsyncSession, provider: str, provider_user_id: str, email: str, username: str):
    user = await get_or_create_oauth_user(db, provider, provider_user_id, email, username)
    redirect = RedirectResponse(url=f"{settings.frontend_url}/#/login?status=success")
    set_auth_cookies(redirect, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return redirect


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, body.email, body.username, body.password)
    set_auth_cookies(response, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return user


@router.post("/login", response_model=UserResponse)
async def login(body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await login_user(db, body.email, body.password)
    set_auth_cookies(response, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return user


@router.post("/logout")
async def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Logged out"}


@router.post("/refresh")
async def refresh(
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    result = await db.execute(select(User).where(User.id == payload["sub"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    response.set_cookie(
        "access_token", create_access_token(str(user.id)),
        httponly=True, secure=True, samesite="none",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return {"message": "Token refreshed"}


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/google", name="google_login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="OAuth state invalid or expired")

    user_info = token.get("userinfo") or {}
    email = user_info.get("email", "")
    provider_user_id = user_info.get("sub", "")
    if not provider_user_id:
        raise HTTPException(status_code=400, detail="Invalid token: missing subject")
    username = user_info.get("name") or email.split("@")[0]

    return await _oauth_redirect(db, "google", provider_user_id, email, username)


@router.get("/github", name="github_login")
async def github_login(request: Request):
    redirect_uri = str(request.url_for("github_callback"))
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback", name="github_callback")
async def github_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.github.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="OAuth state invalid or expired")

    resp = await oauth.github.get("user", token=token)
    user_info = resp.json()
    provider_user_id = str(user_info["id"])
    username = user_info.get("login", "user")
    email = user_info.get("email")

    if not email:
        emails_resp = await oauth.github.get("user/emails", token=token)
        emails = emails_resp.json()
        primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
        email = primary["email"] if primary else f"{provider_user_id}@github.users.noreply.com"

    return await _oauth_redirect(db, "github", provider_user_id, email, username)
