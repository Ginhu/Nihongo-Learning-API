from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.database import get_db
from app.models.activity import CharacterStats, QuizHistory
from app.models.user import User, UserProgress
from app.schemas.progress import (
    CharacterStatsItem, ProgressResponse, QuizHistoryItem,
    QuizResult, QuizSubmit, VocabQuizSubmit,
)
from app.services.progress_service import apply_quiz_result, compute_level

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressResponse)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserProgress).where(UserProgress.user_id == current_user.id))
    prog = result.scalar_one()
    return ProgressResponse(
        xp=prog.xp,
        streak=prog.streak,
        level=compute_level(prog.xp),
        last_played_date=prog.last_played_date,
    )


@router.post("/quiz", response_model=QuizResult)
async def submit_quiz(
    body: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await apply_quiz_result(db, current_user.id, body.mode, body.score, body.total, body.answers)


@router.post("/vocab-quiz", response_model=QuizResult)
async def submit_vocab_quiz(
    body: VocabQuizSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await apply_quiz_result(
        db, current_user.id, body.mode, body.score, body.total, [], xp_override=body.xp_total
    )


@router.get("/history", response_model=List[QuizHistoryItem])
async def get_history(
    mode: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(QuizHistory)
        .where(QuizHistory.user_id == current_user.id)
        .order_by(QuizHistory.played_at.desc())
    )
    if mode:
        stmt = stmt.where(QuizHistory.mode == mode)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/character-stats", response_model=List[CharacterStatsItem])
async def get_character_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CharacterStats).where(CharacterStats.user_id == current_user.id)
    )
    return result.scalars().all()
