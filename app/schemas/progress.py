from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date


class AnswerItem(BaseModel):
    char_key: str
    was_correct: bool


class QuizSubmit(BaseModel):
    mode: str
    score: int
    total: int
    answers: List[AnswerItem]


class VocabQuizSubmit(BaseModel):
    mode: str
    score: int
    total: int
    xp_total: int


class QuizResult(BaseModel):
    xp_gained: int
    new_level: Optional[int] = None


class ProgressResponse(BaseModel):
    xp: int
    streak: int
    level: int
    last_played_date: Optional[date] = None


class QuizHistoryItem(BaseModel):
    id: UUID
    mode: str
    score: int
    total: int
    xp_gained: int
    played_at: datetime

    model_config = {"from_attributes": True}


class CharacterStatsItem(BaseModel):
    char_key: str
    correct: int
    incorrect: int

    model_config = {"from_attributes": True}
