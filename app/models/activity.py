import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, ForeignKey, Index, PrimaryKeyConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class QuizHistory(Base):
    __tablename__ = "quiz_history"
    __table_args__ = (Index("ix_quiz_history_user_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    mode: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    xp_gained: Mapped[int] = mapped_column(Integer, nullable=False)
    played_at: Mapped[datetime] = mapped_column(server_default=text("now()"))


class CharacterStats(Base):
    __tablename__ = "character_stats"
    __table_args__ = (PrimaryKeyConstraint("user_id", "char_key"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    char_key: Mapped[str] = mapped_column(String, nullable=False)
    correct: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    incorrect: Mapped[int] = mapped_column(Integer, default=0, server_default="0")


class FlashcardKnown(Base):
    __tablename__ = "flashcard_known"
    __table_args__ = (PrimaryKeyConstraint("user_id", "card_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    card_id: Mapped[str] = mapped_column(String, nullable=False)
    known: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Favorites(Base):
    __tablename__ = "favorites"
    __table_args__ = (PrimaryKeyConstraint("user_id", "item_type", "item_key"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    item_type: Mapped[str] = mapped_column(String, nullable=False)  # 'kanji' or 'vocabulary'
    item_key: Mapped[str] = mapped_column(String, nullable=False)
