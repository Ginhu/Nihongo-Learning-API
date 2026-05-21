from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.content import Kana, Kanji, Vocabulary
from app.schemas.content import KanaResponse, KanjiResponse, VocabularyResponse

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/kana", response_model=List[KanaResponse])
async def get_kana(
    type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Kana)
    if type:
        stmt = stmt.where(Kana.type == type)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/vocabulary")
async def get_vocabulary(
    jlpt: Optional[str] = Query(None),
    lang: str = Query("en"),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Vocabulary)
    if jlpt and jlpt != "all":
        stmt = stmt.where(Vocabulary.jlpt == jlpt)
    if category and category != "all":
        stmt = stmt.where(Vocabulary.category == category)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return [
        VocabularyResponse(
            id=v.id,
            expression=v.expression,
            reading=v.reading,
            meaning=(v.meaning_pt or v.meaning) if lang == "pt" else v.meaning,
            jlpt=v.jlpt,
            pos=v.pos,
            category=v.category,
        )
        for v in items
    ]


@router.get("/kanji")
async def get_kanji(
    jlpt: Optional[str] = Query(None),
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Kanji)
    if jlpt and jlpt != "all":
        stmt = stmt.where(Kanji.jlpt == jlpt)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return [
        KanjiResponse(
            id=k.id,
            kanji=k.kanji,
            meaning=(k.meaning_pt or k.meaning) if lang == "pt" else k.meaning,
            onyomi=k.onyomi,
            kunyomi=k.kunyomi,
            jlpt=k.jlpt,
            stroke_count=k.stroke_count,
            examples=k.examples,
        )
        for k in items
    ]
