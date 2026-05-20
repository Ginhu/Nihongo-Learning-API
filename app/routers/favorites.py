import uuid
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.database import get_db
from app.models.activity import Favorites
from app.models.user import User
from app.schemas.favorites import FavoritesResponse, ToggleResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("", response_model=FavoritesResponse)
async def get_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Favorites).where(Favorites.user_id == current_user.id))
    items = result.scalars().all()
    return FavoritesResponse(
        kanji=[f.item_key for f in items if f.item_type == "kanji"],
        vocabulary=[f.item_key for f in items if f.item_type == "vocabulary"],
    )


async def _toggle(db: AsyncSession, user_id: uuid.UUID, item_type: str, item_key: str) -> ToggleResponse:
    result = await db.execute(
        select(Favorites).where(
            Favorites.user_id == user_id,
            Favorites.item_type == item_type,
            Favorites.item_key == item_key,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        await db.delete(existing)
        await db.commit()
        return ToggleResponse(favorited=False)
    db.add(Favorites(user_id=user_id, item_type=item_type, item_key=item_key))
    await db.commit()
    return ToggleResponse(favorited=True)


@router.post("/kanji/{kanji}", response_model=ToggleResponse)
async def toggle_kanji(
    kanji: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await _toggle(db, current_user.id, "kanji", kanji)


@router.post("/vocabulary/{key}", response_model=ToggleResponse)
async def toggle_vocabulary(
    key: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await _toggle(db, current_user.id, "vocabulary", key)
