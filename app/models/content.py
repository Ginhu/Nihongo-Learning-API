from sqlalchemy import String, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Kana(Base):
    __tablename__ = "kana"
    __table_args__ = (UniqueConstraint("kana", "type"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kana: Mapped[str] = mapped_column(String, nullable=False)
    romaji: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # 'hiragana' or 'katakana'
    grp: Mapped[str] = mapped_column(String, nullable=False)


class Vocabulary(Base):
    __tablename__ = "vocabulary"
    __table_args__ = (UniqueConstraint("expression", "reading"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    expression: Mapped[str] = mapped_column(String, nullable=False)
    reading: Mapped[str] = mapped_column(String, nullable=False)
    meaning: Mapped[str] = mapped_column(Text, nullable=False)
    meaning_pt: Mapped[str | None] = mapped_column(Text, nullable=True)
    jlpt: Mapped[str] = mapped_column(String, nullable=False)
    pos: Mapped[str | None] = mapped_column(String, nullable=True)
    category: Mapped[str | None] = mapped_column(String, nullable=True)


class Kanji(Base):
    __tablename__ = "kanji"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kanji: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    meaning: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    meaning_pt: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    onyomi: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    kunyomi: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    jlpt: Mapped[str] = mapped_column(String, nullable=False)
    stroke_count: Mapped[int] = mapped_column(Integer, nullable=False)
    examples: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
