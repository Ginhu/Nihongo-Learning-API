from pydantic import BaseModel
from typing import Optional, List


class KanaResponse(BaseModel):
    id: int
    kana: str
    romaji: str
    type: str
    grp: str

    model_config = {"from_attributes": True}


class VocabularyResponse(BaseModel):
    id: int
    expression: str
    reading: str
    meaning: str
    jlpt: str
    pos: Optional[str] = None
    category: Optional[str] = None


class KanjiResponse(BaseModel):
    id: int
    kanji: str
    meaning: List[str]
    onyomi: List[str]
    kunyomi: List[str]
    jlpt: str
    stroke_count: int
    examples: List[dict]
