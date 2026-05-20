from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.database import get_db
from app.models.activity import FlashcardKnown
from app.models.user import User
from app.schemas.flashcards import FlashcardKnownResponse

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("/known", response_model=List[FlashcardKnownResponse])
async def get_known(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FlashcardKnown).where(FlashcardKnown.user_id == current_user.id)
    )
    return result.scalars().all()


@router.put("/known/{card_id}", response_model=FlashcardKnownResponse)
async def mark_known(
    card_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        pg_insert(FlashcardKnown)
        .values(user_id=current_user.id, card_id=card_id, known=True)
        .on_conflict_do_update(
            index_elements=["user_id", "card_id"],
            set_={"known": True},
        )
        .returning(FlashcardKnown)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()


@router.delete("/known/{card_id}", status_code=204)
async def unmark_known(
    card_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FlashcardKnown).where(
            FlashcardKnown.user_id == current_user.id,
            FlashcardKnown.card_id == card_id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
