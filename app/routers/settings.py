from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User, UserSettings
from app.schemas.settings import SettingsPatch, SettingsResponse

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == current_user.id))
    return result.scalar_one()


@router.patch("", response_model=SettingsResponse)
async def patch_settings(
    body: SettingsPatch,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == current_user.id))
    user_settings = result.scalar_one()
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(user_settings, field, value)
    await db.commit()
    await db.refresh(user_settings)
    return user_settings
