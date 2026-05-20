import uuid
from datetime import date, timedelta
from math import floor
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models.user import UserProgress
from app.models.activity import QuizHistory, CharacterStats

MAX_LEVEL = 10


def compute_level(xp: int) -> int:
    return min(floor(xp / 500) + 1, MAX_LEVEL)


def calculate_xp_gained(score: int, total: int, answers: list) -> int:
    correct_count = sum(1 for a in answers if a.was_correct)
    return correct_count * 10 + (50 if score == total else 0)


def calculate_streak(last_played: Optional[date], today: date, current_streak: int) -> int:
    if last_played is None or last_played < today - timedelta(days=1):
        return 1
    if last_played == today - timedelta(days=1):
        return current_streak + 1
    return current_streak  # already played today


async def apply_quiz_result(
    db: AsyncSession,
    user_id: uuid.UUID,
    mode: str,
    score: int,
    total: int,
    answers: list,
    xp_override: Optional[int] = None,
) -> dict:
    result = await db.execute(select(UserProgress).where(UserProgress.user_id == user_id))
    progress = result.scalar_one()

    prev_xp = progress.xp
    prev_level = compute_level(prev_xp)

    xp_gained = xp_override if xp_override is not None else calculate_xp_gained(score, total, answers)
    progress.xp += xp_gained

    today = date.today()
    progress.streak = calculate_streak(progress.last_played_date, today, progress.streak)
    progress.last_played_date = today

    new_level = compute_level(progress.xp)
    level_up = new_level if new_level > prev_level else None

    db.add(QuizHistory(
        user_id=user_id, mode=mode, score=score, total=total, xp_gained=xp_gained
    ))

    for answer in answers:
        stmt = pg_insert(CharacterStats).values(
            user_id=user_id,
            char_key=answer.char_key,
            correct=1 if answer.was_correct else 0,
            incorrect=0 if answer.was_correct else 1,
        ).on_conflict_do_update(
            index_elements=["user_id", "char_key"],
            set_={
                "correct": CharacterStats.correct + (1 if answer.was_correct else 0),
                "incorrect": CharacterStats.incorrect + (0 if answer.was_correct else 1),
            },
        )
        await db.execute(stmt)

    await db.commit()
    return {"xp_gained": xp_gained, "new_level": level_up}
