# Nihongo Master API — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-ready FastAPI backend for the Nihongo Master Japanese learning app, deployable to Render with PostgreSQL 16.

**Architecture:** Async FastAPI with SQLAlchemy 2.x (asyncpg). Auth via JWT httpOnly cookies + OAuth (Google/GitHub). All business logic in service layer; routers are thin. Single Alembic migration creates the full schema; `seed.py` populates reference data idempotently.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.x async, asyncpg, Alembic, python-jose, passlib[bcrypt], authlib, pydantic-settings, uvicorn, pytest, pytest-asyncio, httpx

---

## File Map

```
app/
  __init__.py
  main.py                      — app factory, middleware, router mounts
  database.py                  — engine, session factory, Base, get_db
  core/
    __init__.py
    config.py                  — Pydantic BaseSettings
    security.py                — JWT, bcrypt, cookie helpers
    deps.py                    — get_current_user FastAPI dependency
  models/
    __init__.py
    user.py                    — User, OAuthAccount, UserSettings, UserProgress
    content.py                 — Kana, Vocabulary, Kanji
    activity.py                — QuizHistory, CharacterStats, FlashcardKnown, Favorites
  schemas/
    __init__.py
    auth.py
    content.py
    settings.py
    progress.py
    flashcards.py
    favorites.py
  routers/
    __init__.py
    auth.py
    content.py
    settings.py
    progress.py
    flashcards.py
    favorites.py
  services/
    __init__.py
    auth_service.py
    progress_service.py
alembic/
  env.py
  script.py.mako
  versions/
    0001_initial_schema.py
tests/
  __init__.py
  conftest.py
  test_auth.py
  test_progress_service.py
  test_content.py
  test_settings.py
  test_progress.py
  test_flashcards.py
  test_favorites.py
seed.py
requirements.txt
.env.example
alembic.ini
render.yaml
README.md
```

---

## Task 1: Bootstrap — requirements.txt, .env.example, empty packages

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `app/__init__.py`, `app/core/__init__.py`, `app/models/__init__.py`, `app/schemas/__init__.py`, `app/routers/__init__.py`, `app/services/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create `requirements.txt`**

```
fastapi==0.115.5
uvicorn[standard]==0.32.1
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.14.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
authlib==1.3.2
httpx==0.28.0
pydantic-settings==2.6.1
pydantic[email]==2.10.2
starlette==0.41.3
pytest==8.3.4
pytest-asyncio==0.24.0
pytest-httpx==0.34.0
```

- [ ] **Step 2: Create `.env.example`**

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/nihongo
SECRET_KEY=changeme32byteshexstringhere1234
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
FRONTEND_URL=https://ginhu.github.io/Nihongo-Learning
```

- [ ] **Step 3: Create all `__init__.py` files (empty)**

```bash
touch app/__init__.py app/core/__init__.py app/models/__init__.py \
  app/schemas/__init__.py app/routers/__init__.py app/services/__init__.py \
  tests/__init__.py
```

- [ ] **Step 4: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: all packages install without error.

- [ ] **Step 5: Commit**

```bash
git init
git add requirements.txt .env.example app/ tests/
git commit -m "chore: bootstrap project structure"
```

---

## Task 2: Core Config & Security

**Files:**
- Create: `app/core/config.py`
- Create: `app/core/security.py`
- Create: `.env` (from `.env.example`, not committed)
- Create: `tests/test_security.py`

- [ ] **Step 1: Write failing test for security helpers**

Create `tests/test_security.py`:

```python
import pytest
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)

def test_hash_and_verify_password():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_and_decode_access_token():
    token = create_access_token("user-123")
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "access"

def test_create_and_decode_refresh_token():
    token = create_refresh_token("user-123")
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "refresh"

def test_decode_invalid_token_raises():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        decode_token("not.a.valid.token")
    assert exc.value.status_code == 401
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
pytest tests/test_security.py -v
```

Expected: `ImportError` — `app.core.security` not found.

- [ ] **Step 3: Create `app/core/config.py`**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    frontend_url: str = "https://ginhu.github.io/Nihongo-Learning"

    model_config = {"env_file": ".env"}


settings = Settings()
```

- [ ] **Step 4: Create `app/core/security.py`**

```python
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "type": "access"},
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "type": "refresh"},
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def set_auth_cookies(response, access_token: str, refresh_token: str) -> None:
    opts = dict(httponly=True, secure=True, samesite="none")
    response.set_cookie(
        "access_token", access_token,
        max_age=settings.access_token_expire_minutes * 60, **opts
    )
    response.set_cookie(
        "refresh_token", refresh_token,
        max_age=settings.refresh_token_expire_days * 86400, **opts
    )


def clear_auth_cookies(response) -> None:
    opts = dict(httponly=True, secure=True, samesite="none")
    response.delete_cookie("access_token", **opts)
    response.delete_cookie("refresh_token", **opts)
```

- [ ] **Step 5: Create `.env` file** (copy `.env.example`, fill real `SECRET_KEY` and `DATABASE_URL`)

```bash
cp .env.example .env
# Edit .env: set DATABASE_URL to your local PostgreSQL, set SECRET_KEY to a 32-char hex string
```

- [ ] **Step 6: Run tests and confirm they pass**

```bash
pytest tests/test_security.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add app/core/config.py app/core/security.py tests/test_security.py .env.example
git commit -m "feat: core config and security helpers"
```

---

## Task 3: Database Setup

**Files:**
- Create: `app/database.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Create `app/database.py`**

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

- [ ] **Step 2: Create `tests/conftest.py`**

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
import os

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/nihongo_test",
)

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    from app.database import Base
    import app.models.user  # noqa
    import app.models.content  # noqa
    import app.models.activity  # noqa

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def clean_users():
    yield
    async with TestSessionLocal() as session:
        await session.execute(text("TRUNCATE users RESTART IDENTITY CASCADE"))
        await session.commit()


@pytest_asyncio.fixture
async def client():
    from app.main import app
    from app.database import get_db

    async def override_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db():
    async with TestSessionLocal() as session:
        yield session
```

- [ ] **Step 3: Create test PostgreSQL database**

```bash
psql -U postgres -c "CREATE DATABASE nihongo_test;"
```

- [ ] **Step 4: Commit**

```bash
git add app/database.py tests/conftest.py
git commit -m "feat: async database setup and test fixtures"
```

---

## Task 4: SQLAlchemy Models

**Files:**
- Create: `app/models/user.py`
- Create: `app/models/content.py`
- Create: `app/models/activity.py`

- [ ] **Step 1: Create `app/models/user.py`**

```python
import uuid
from datetime import datetime, date
from sqlalchemy import String, Boolean, Integer, Date, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("now()"), onupdate=datetime.utcnow
    )


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    __table_args__ = (UniqueConstraint("provider", "provider_user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String, nullable=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    quiz_length: Mapped[int] = mapped_column(Integer, default=10, server_default="10")
    romaji_visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    sound_enabled: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    theme: Mapped[str] = mapped_column(String, default="dark", server_default="'dark'")
    language: Mapped[str] = mapped_column(String, default="en", server_default="'en'")


class UserProgress(Base):
    __tablename__ = "user_progress"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    xp: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    streak: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    last_played_date: Mapped[date | None] = mapped_column(Date, nullable=True)
```

- [ ] **Step 2: Create `app/models/content.py`**

```python
from sqlalchemy import String, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Kana(Base):
    __tablename__ = "kana"

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
    examples: Mapped[list] = mapped_column(JSONB, nullable=False)
```

- [ ] **Step 3: Create `app/models/activity.py`**

```python
import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, ForeignKey, PrimaryKeyConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class QuizHistory(Base):
    __tablename__ = "quiz_history"

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
```

- [ ] **Step 4: Verify models import cleanly**

```bash
python -c "import app.models.user, app.models.content, app.models.activity; print('OK')"
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add app/models/
git commit -m "feat: SQLAlchemy models for all tables"
```

---

## Task 5: Alembic Migration

**Files:**
- Create: `alembic.ini`
- Create: `alembic/env.py`
- Create: `alembic/script.py.mako`
- Create: `alembic/versions/0001_initial_schema.py`

- [ ] **Step 1: Initialize Alembic**

```bash
alembic init alembic
```

This creates `alembic.ini` and `alembic/` directory.

- [ ] **Step 2: Replace `alembic/env.py` with async version**

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.core.config import settings
from app.database import Base
import app.models.user  # noqa — must import to register metadata
import app.models.content  # noqa
import app.models.activity  # noqa

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: Generate initial migration**

```bash
alembic revision --autogenerate -m "initial schema"
```

Expected: creates `alembic/versions/<hash>_initial_schema.py`. Review it to confirm all 11 tables are present (users, oauth_accounts, user_settings, user_progress, quiz_history, character_stats, flashcard_known, favorites, kana, vocabulary, kanji).

- [ ] **Step 4: Rename the generated file for clarity**

```bash
# Rename the generated file to a predictable name (optional but clean)
# e.g. mv alembic/versions/abc123_initial_schema.py alembic/versions/0001_initial_schema.py
# Update the "Revision ID" in the file header to match the new filename if renamed
```

- [ ] **Step 5: Create the local database and run the migration**

```bash
psql -U postgres -c "CREATE DATABASE nihongo;"
alembic upgrade head
```

Expected: migration runs without error. Verify with:

```bash
psql -U postgres -d nihongo -c "\dt"
```

Expected: 11 tables listed.

- [ ] **Step 6: Commit**

```bash
git add alembic/ alembic.ini
git commit -m "feat: initial schema migration"
```

---

## Task 6: Pydantic Schemas

**Files:**
- Create: `app/schemas/auth.py`
- Create: `app/schemas/content.py`
- Create: `app/schemas/settings.py`
- Create: `app/schemas/progress.py`
- Create: `app/schemas/flashcards.py`
- Create: `app/schemas/favorites.py`

- [ ] **Step 1: Create `app/schemas/auth.py`**

```python
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: Create `app/schemas/content.py`**

```python
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
    examples: list
```

- [ ] **Step 3: Create `app/schemas/settings.py`**

```python
from pydantic import BaseModel
from typing import Optional


class SettingsResponse(BaseModel):
    quiz_length: int
    romaji_visible: bool
    sound_enabled: bool
    theme: str
    language: str

    model_config = {"from_attributes": True}


class SettingsPatch(BaseModel):
    quiz_length: Optional[int] = None
    romaji_visible: Optional[bool] = None
    sound_enabled: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None
```

- [ ] **Step 4: Create `app/schemas/progress.py`**

```python
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
```

- [ ] **Step 5: Create `app/schemas/flashcards.py`**

```python
from pydantic import BaseModel
from uuid import UUID


class FlashcardKnownResponse(BaseModel):
    card_id: str
    known: bool

    model_config = {"from_attributes": True}
```

- [ ] **Step 6: Create `app/schemas/favorites.py`**

```python
from pydantic import BaseModel
from typing import List


class FavoritesResponse(BaseModel):
    kanji: List[str]
    vocabulary: List[str]


class ToggleResponse(BaseModel):
    favorited: bool
```

- [ ] **Step 7: Verify schemas import cleanly**

```bash
python -c "import app.schemas.auth, app.schemas.content, app.schemas.settings, app.schemas.progress, app.schemas.flashcards, app.schemas.favorites; print('OK')"
```

Expected: `OK`

- [ ] **Step 8: Commit**

```bash
git add app/schemas/
git commit -m "feat: Pydantic schemas for all domains"
```

---

## Task 7: Progress Service (Pure Logic + Unit Tests)

**Files:**
- Create: `app/services/progress_service.py`
- Create: `tests/test_progress_service.py`

- [ ] **Step 1: Write failing unit tests**

Create `tests/test_progress_service.py`:

```python
from datetime import date, timedelta
from app.services.progress_service import calculate_xp_gained, calculate_streak, compute_level


class TestCalculateXpGained:
    def test_correct_answers_give_10_each(self):
        answers = [
            type("A", (), {"was_correct": True})(),
            type("A", (), {"was_correct": True})(),
            type("A", (), {"was_correct": False})(),
        ]
        assert calculate_xp_gained(score=2, total=3, answers=answers) == 20

    def test_perfect_score_adds_50_bonus(self):
        answers = [type("A", (), {"was_correct": True})() for _ in range(3)]
        assert calculate_xp_gained(score=3, total=3, answers=answers) == 80  # 30 + 50

    def test_zero_correct_no_perfect_bonus(self):
        answers = [type("A", (), {"was_correct": False})() for _ in range(5)]
        assert calculate_xp_gained(score=0, total=5, answers=answers) == 0


class TestCalculateStreak:
    def test_first_play_sets_streak_to_1(self):
        today = date.today()
        assert calculate_streak(last_played=None, today=today, current_streak=0) == 1

    def test_consecutive_day_increments_streak(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        assert calculate_streak(last_played=yesterday, today=today, current_streak=5) == 6

    def test_same_day_keeps_streak(self):
        today = date.today()
        assert calculate_streak(last_played=today, today=today, current_streak=3) == 3

    def test_gap_resets_streak_to_1(self):
        today = date.today()
        two_days_ago = today - timedelta(days=2)
        assert calculate_streak(last_played=two_days_ago, today=today, current_streak=10) == 1


class TestComputeLevel:
    def test_zero_xp_is_level_1(self):
        assert compute_level(0) == 1

    def test_499_xp_is_level_1(self):
        assert compute_level(499) == 1

    def test_500_xp_is_level_2(self):
        assert compute_level(500) == 2

    def test_999_xp_is_level_2(self):
        assert compute_level(999) == 2

    def test_level_capped_at_10(self):
        assert compute_level(4500) == 10
        assert compute_level(99999) == 10
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/test_progress_service.py -v
```

Expected: `ImportError` — module not found.

- [ ] **Step 3: Create `app/services/progress_service.py`**

```python
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
    user_id,
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
```

- [ ] **Step 4: Run tests and confirm they pass**

```bash
pytest tests/test_progress_service.py -v
```

Expected: 11 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/services/progress_service.py tests/test_progress_service.py
git commit -m "feat: progress service with XP, streak, and level logic"
```

---

## Task 8: Auth Service

**Files:**
- Create: `app/services/auth_service.py`

- [ ] **Step 1: Create `app/services/auth_service.py`**

```python
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User, OAuthAccount, UserSettings, UserProgress
from app.core.security import hash_password, verify_password


async def register_user(db: AsyncSession, email: str, username: str, password: str) -> User:
    if await _email_exists(db, email):
        raise HTTPException(status_code=409, detail="Email already registered")
    if await _username_exists(db, username):
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(email=email, username=username, password_hash=hash_password(password))
    db.add(user)
    await db.flush()
    await _create_user_defaults(db, user.id)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, email: str, password: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


async def get_or_create_oauth_user(
    db: AsyncSession,
    provider: str,
    provider_user_id: str,
    email: str,
    username: str,
) -> User:
    result = await db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id,
        )
    )
    oauth_account = result.scalar_one_or_none()

    if oauth_account:
        result = await db.execute(select(User).where(User.id == oauth_account.user_id))
        return result.scalar_one()

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        safe_username = await _unique_username(db, username)
        user = User(email=email, username=safe_username)
        db.add(user)
        await db.flush()
        await _create_user_defaults(db, user.id)

    db.add(OAuthAccount(user_id=user.id, provider=provider, provider_user_id=provider_user_id))
    await db.commit()
    await db.refresh(user)
    return user


async def _email_exists(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None


async def _username_exists(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none() is not None


async def _unique_username(db: AsyncSession, base: str) -> str:
    candidate = base.replace(" ", "_").lower()[:30]
    counter = 0
    while await _username_exists(db, candidate):
        counter += 1
        candidate = f"{base[:27]}_{counter}"
    return candidate


async def _create_user_defaults(db: AsyncSession, user_id: uuid.UUID) -> None:
    db.add(UserSettings(user_id=user_id))
    db.add(UserProgress(user_id=user_id))
```

- [ ] **Step 2: Verify import**

```bash
python -c "from app.services.auth_service import register_user; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add app/services/auth_service.py
git commit -m "feat: auth service — register, login, OAuth upsert"
```

---

## Task 9: Auth Router (email+password) + Auth Dependency + main.py skeleton

**Files:**
- Create: `app/core/deps.py`
- Create: `app/routers/auth.py`
- Create: `app/main.py`
- Create: `tests/test_auth.py`

- [ ] **Step 1: Create `app/core/deps.py`**

```python
from typing import Optional
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.core.security import decode_token
from app.models.user import User


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    access_token: Optional[str] = Cookie(default=None),
) -> User:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token(access_token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    result = await db.execute(select(User).where(User.id == payload["sub"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
```

- [ ] **Step 2: Create `app/routers/auth.py`**

```python
from typing import Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.core.security import (
    create_access_token, create_refresh_token, decode_token,
    set_auth_cookies, clear_auth_cookies,
)
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, body.email, body.username, body.password)
    set_auth_cookies(response, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return user


@router.post("/login", response_model=UserResponse)
async def login(body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await login_user(db, body.email, body.password)
    set_auth_cookies(response, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return user


@router.post("/logout")
async def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Logged out"}


@router.post("/refresh")
async def refresh(
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    result = await db.execute(select(User).where(User.id == payload["sub"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    response.set_cookie(
        "access_token", create_access_token(str(user.id)),
        httponly=True, secure=True, samesite="none",
        max_age=60 * 60,
    )
    return {"message": "Token refreshed"}


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
```

- [ ] **Step 3: Create `app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.routers import auth, content, settings as settings_router, progress, flashcards, favorites

app = FastAPI(title="Nihongo Master API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "https://ginhu.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(settings_router.router)
app.include_router(progress.router)
app.include_router(flashcards.router)
app.include_router(favorites.router)
```

Note: The remaining routers (content, settings, progress, flashcards, favorites) don't exist yet — create them as empty stubs so `main.py` imports without error:

```python
# app/routers/content.py (stub)
from fastapi import APIRouter
router = APIRouter(prefix="/content", tags=["content"])
```

Repeat for `settings.py`, `progress.py`, `flashcards.py`, `favorites.py` stubs.

- [ ] **Step 4: Write failing auth tests**

Create `tests/test_auth.py`:

```python
import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_register_creates_user(client):
    resp = await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "secret123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "access_token" in resp.cookies


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client):
    body = {"email": "dup@example.com", "username": "user1", "password": "pass"}
    await client.post("/auth/register", json=body)
    resp = await client.post("/auth/register", json={**body, "username": "user2"})
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_user(client):
    await client.post("/auth/register", json={
        "email": "login@example.com", "username": "loginuser", "password": "pass123",
    })
    resp = await client.post("/auth/login", json={
        "email": "login@example.com", "password": "pass123",
    })
    assert resp.status_code == 200
    assert resp.json()["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(client):
    await client.post("/auth/register", json={
        "email": "wp@example.com", "username": "wpuser", "password": "correct",
    })
    resp = await client.post("/auth/login", json={"email": "wp@example.com", "password": "wrong"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_current_user(client):
    await client.post("/auth/register", json={
        "email": "me@example.com", "username": "meuser", "password": "pass",
    })
    resp = await client.get("/auth/me")
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_logout_clears_cookies(client):
    await client.post("/auth/register", json={
        "email": "lo@example.com", "username": "louser", "password": "pass",
    })
    resp = await client.post("/auth/logout")
    assert resp.status_code == 200
    resp2 = await client.get("/auth/me")
    assert resp2.status_code == 401
```

- [ ] **Step 5: Run auth tests**

```bash
pytest tests/test_auth.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add app/core/deps.py app/routers/auth.py app/routers/ app/main.py tests/test_auth.py
git commit -m "feat: auth router — register, login, logout, refresh, me"
```

---

## Task 10: OAuth (Google + GitHub)

**Files:**
- Modify: `app/routers/auth.py`

- [ ] **Step 1: Add OAuth setup to `app/routers/auth.py`**

Add the following at the top of `app/routers/auth.py`, after existing imports:

```python
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.services.auth_service import get_or_create_oauth_user

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
oauth.register(
    name="github",
    client_id=settings.github_client_id,
    client_secret=settings.github_client_secret,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
```

Add `from app.core.config import settings` if not already imported.

- [ ] **Step 2: Add OAuth endpoints to `app/routers/auth.py`**

Append to `app/routers/auth.py`:

```python
@router.get("/google", name="google_login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="OAuth state invalid or expired")

    user_info = token.get("userinfo") or {}
    email = user_info.get("email", "")
    provider_user_id = user_info.get("sub", "")
    username = user_info.get("name", email.split("@")[0])

    user = await get_or_create_oauth_user(db, "google", provider_user_id, email, username)
    redirect = RedirectResponse(url=f"{settings.frontend_url}/#/login?status=success")
    set_auth_cookies(redirect, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return redirect


@router.get("/github", name="github_login")
async def github_login(request: Request):
    redirect_uri = str(request.url_for("github_callback"))
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback", name="github_callback")
async def github_callback(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    try:
        token = await oauth.github.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="OAuth state invalid or expired")

    resp = await oauth.github.get("user", token=token)
    user_info = resp.json()
    provider_user_id = str(user_info["id"])
    username = user_info.get("login", "user")
    email = user_info.get("email")

    if not email:
        emails_resp = await oauth.github.get("user/emails", token=token)
        emails = emails_resp.json()
        primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
        email = primary["email"] if primary else f"{provider_user_id}@github.users.noreply.com"

    user = await get_or_create_oauth_user(db, "github", provider_user_id, email, username)
    redirect = RedirectResponse(url=f"{settings.frontend_url}/#/login?status=success")
    set_auth_cookies(redirect, create_access_token(str(user.id)), create_refresh_token(str(user.id)))
    return redirect
```

- [ ] **Step 3: Verify the app starts**

```bash
uvicorn app.main:app --reload
```

Expected: server starts on port 8000 without errors. Visit `http://localhost:8000/docs` to confirm OAuth routes appear.

- [ ] **Step 4: Commit**

```bash
git add app/routers/auth.py
git commit -m "feat: Google and GitHub OAuth callbacks"
```

---

## Task 11: Content Router

**Files:**
- Modify: `app/routers/content.py`
- Create: `tests/test_content.py`

- [ ] **Step 1: Write failing content tests**

Create `tests/test_content.py`:

```python
import pytest
import pytest_asyncio
from app.models.content import Kana, Vocabulary, Kanji


@pytest_asyncio.fixture(autouse=True)
async def seed_content(db):
    db.add(Kana(kana="あ", romaji="a", type="hiragana", grp="vowel"))
    db.add(Kana(kana="ア", romaji="a", type="katakana", grp="vowel"))
    db.add(Vocabulary(expression="今", reading="いま", meaning="now", jlpt="N5", category="time"))
    db.add(Vocabulary(expression="水", reading="みず", meaning="water", meaning_pt="água", jlpt="N5", category="nature"))
    db.add(Kanji(
        kanji="一", meaning=["one"], onyomi=["イチ"], kunyomi=["ひと.つ"],
        jlpt="N5", stroke_count=1, examples=[]
    ))
    await db.commit()


@pytest.mark.asyncio
async def test_get_all_kana(client):
    resp = await client.get("/content/kana")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_kana_filtered_by_type(client):
    resp = await client.get("/content/kana?type=hiragana")
    assert resp.status_code == 200
    assert all(k["type"] == "hiragana" for k in resp.json())


@pytest.mark.asyncio
async def test_get_vocabulary(client):
    resp = await client.get("/content/vocabulary?jlpt=N5")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_vocabulary_lang_pt_fallback(client):
    resp = await client.get("/content/vocabulary?lang=pt")
    data = resp.json()
    agua = next(v for v in data if v["expression"] == "水")
    ima = next(v for v in data if v["expression"] == "今")
    assert agua["meaning"] == "água"
    assert ima["meaning"] == "now"  # fallback since meaning_pt is null


@pytest.mark.asyncio
async def test_get_kanji(client):
    resp = await client.get("/content/kanji?jlpt=N5")
    assert resp.status_code == 200
    assert resp.json()[0]["kanji"] == "一"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/test_content.py -v
```

Expected: tests fail (router is a stub with no routes).

- [ ] **Step 3: Replace stub with full `app/routers/content.py`**

```python
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
    if jlpt:
        stmt = stmt.where(Vocabulary.jlpt == jlpt)
    if category:
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
    if jlpt:
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
```

- [ ] **Step 4: Run tests and confirm they pass**

```bash
pytest tests/test_content.py -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/routers/content.py tests/test_content.py
git commit -m "feat: content router — kana, vocabulary, kanji"
```

---

## Task 12: Settings Router

**Files:**
- Modify: `app/routers/settings.py`
- Create: `tests/test_settings.py`

- [ ] **Step 1: Write failing settings tests**

Create `tests/test_settings.py`:

```python
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "s@example.com", "username": "suser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_get_settings_returns_defaults(auth_client):
    resp = await auth_client.get("/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["quiz_length"] == 10
    assert data["theme"] == "dark"
    assert data["language"] == "en"


@pytest.mark.asyncio
async def test_patch_settings(auth_client):
    resp = await auth_client.patch("/settings", json={"theme": "light", "quiz_length": 20})
    assert resp.status_code == 200
    data = resp.json()
    assert data["theme"] == "light"
    assert data["quiz_length"] == 20
    assert data["language"] == "en"  # unchanged


@pytest.mark.asyncio
async def test_settings_requires_auth(client):
    resp = await client.get("/settings")
    assert resp.status_code == 401
```

- [ ] **Step 2: Run to confirm they fail**

```bash
pytest tests/test_settings.py -v
```

Expected: tests fail (stub router has no routes).

- [ ] **Step 3: Replace stub with full `app/routers/settings.py`**

```python
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
```

- [ ] **Step 4: Run and confirm they pass**

```bash
pytest tests/test_settings.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/routers/settings.py tests/test_settings.py
git commit -m "feat: settings router — get and patch"
```

---

## Task 13: Progress Router

**Files:**
- Modify: `app/routers/progress.py`
- Create: `tests/test_progress.py`

- [ ] **Step 1: Write failing progress tests**

Create `tests/test_progress.py`:

```python
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "p@example.com", "username": "puser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_get_progress_initial(auth_client):
    resp = await auth_client.get("/progress")
    assert resp.status_code == 200
    data = resp.json()
    assert data["xp"] == 0
    assert data["streak"] == 0
    assert data["level"] == 1


@pytest.mark.asyncio
async def test_submit_quiz_updates_xp(auth_client):
    resp = await auth_client.post("/progress/quiz", json={
        "mode": "hiragana",
        "score": 3,
        "total": 3,
        "answers": [
            {"char_key": "あ", "was_correct": True},
            {"char_key": "い", "was_correct": True},
            {"char_key": "う", "was_correct": True},
        ],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["xp_gained"] == 80  # 3*10 + 50 perfect bonus

    progress = await auth_client.get("/progress")
    assert progress.json()["xp"] == 80


@pytest.mark.asyncio
async def test_submit_quiz_level_up(auth_client):
    for _ in range(6):
        await auth_client.post("/progress/quiz", json={
            "mode": "hiragana", "score": 10, "total": 10,
            "answers": [{"char_key": f"k{i}", "was_correct": True} for i in range(10)],
        })
    resp = await auth_client.post("/progress/quiz", json={
        "mode": "hiragana", "score": 10, "total": 10,
        "answers": [{"char_key": f"k{i}", "was_correct": True} for i in range(10)],
    })
    assert resp.json()["new_level"] is not None


@pytest.mark.asyncio
async def test_submit_vocab_quiz(auth_client):
    resp = await auth_client.post("/progress/vocab-quiz", json={
        "mode": "vocab", "score": 5, "total": 10, "xp_total": 50,
    })
    assert resp.status_code == 200
    assert resp.json()["xp_gained"] == 50


@pytest.mark.asyncio
async def test_get_history(auth_client):
    await auth_client.post("/progress/quiz", json={
        "mode": "katakana", "score": 1, "total": 5,
        "answers": [{"char_key": "ア", "was_correct": True}],
    })
    resp = await auth_client.get("/progress/history")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_get_character_stats(auth_client):
    await auth_client.post("/progress/quiz", json={
        "mode": "hiragana", "score": 1, "total": 1,
        "answers": [{"char_key": "あ", "was_correct": True}],
    })
    resp = await auth_client.get("/progress/character-stats")
    assert resp.status_code == 200
    stats = resp.json()
    assert any(s["char_key"] == "あ" and s["correct"] == 1 for s in stats)
```

- [ ] **Step 2: Run to confirm they fail**

```bash
pytest tests/test_progress.py -v
```

Expected: tests fail (stub router).

- [ ] **Step 3: Replace stub with full `app/routers/progress.py`**

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.database import get_db
from app.models.activity import CharacterStats, QuizHistory
from app.models.user import User
from app.schemas.progress import (
    CharacterStatsItem, ProgressResponse, QuizHistoryItem,
    QuizResult, QuizSubmit, VocabQuizSubmit,
)
from app.services.progress_service import apply_quiz_result, compute_level
from app.models.user import UserProgress

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressResponse)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserProgress).where(UserProgress.user_id == current_user.id))
    p = result.scalar_one()
    return ProgressResponse(
        xp=p.xp,
        streak=p.streak,
        level=compute_level(p.xp),
        last_played_date=p.last_played_date,
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
```

- [ ] **Step 4: Run and confirm they pass**

```bash
pytest tests/test_progress.py -v
```

Expected: 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/routers/progress.py tests/test_progress.py
git commit -m "feat: progress router — quiz submission, history, character stats"
```

---

## Task 14: Flashcards Router

**Files:**
- Modify: `app/routers/flashcards.py`
- Create: `tests/test_flashcards.py`

- [ ] **Step 1: Write failing flashcard tests**

Create `tests/test_flashcards.py`:

```python
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "fc@example.com", "username": "fcuser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_known_starts_empty(auth_client):
    resp = await auth_client.get("/flashcards/known")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_put_marks_card_known(auth_client):
    resp = await auth_client.put("/flashcards/known/card-abc")
    assert resp.status_code == 200
    assert resp.json()["known"] is True

    resp2 = await auth_client.get("/flashcards/known")
    assert any(c["card_id"] == "card-abc" for c in resp2.json())


@pytest.mark.asyncio
async def test_delete_removes_card(auth_client):
    await auth_client.put("/flashcards/known/card-del")
    resp = await auth_client.delete("/flashcards/known/card-del")
    assert resp.status_code == 204

    resp2 = await auth_client.get("/flashcards/known")
    assert not any(c["card_id"] == "card-del" for c in resp2.json())


@pytest.mark.asyncio
async def test_delete_nonexistent_returns_404(auth_client):
    resp = await auth_client.delete("/flashcards/known/does-not-exist")
    assert resp.status_code == 404
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_flashcards.py -v
```

- [ ] **Step 3: Replace stub with full `app/routers/flashcards.py`**

```python
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
```

- [ ] **Step 4: Run and confirm they pass**

```bash
pytest tests/test_flashcards.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/routers/flashcards.py tests/test_flashcards.py
git commit -m "feat: flashcards router — known cards CRUD"
```

---

## Task 15: Favorites Router

**Files:**
- Modify: `app/routers/favorites.py`
- Create: `tests/test_favorites.py`

- [ ] **Step 1: Write failing favorites tests**

Create `tests/test_favorites.py`:

```python
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "fav@example.com", "username": "favuser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_favorites_start_empty(auth_client):
    resp = await auth_client.get("/favorites")
    assert resp.status_code == 200
    assert resp.json() == {"kanji": [], "vocabulary": []}


@pytest.mark.asyncio
async def test_toggle_kanji_adds_favorite(auth_client):
    resp = await auth_client.post("/favorites/kanji/%E4%B8%80")  # URL-encoded 一
    assert resp.status_code == 200
    assert resp.json()["favorited"] is True

    resp2 = await auth_client.get("/favorites")
    assert "一" in resp2.json()["kanji"]


@pytest.mark.asyncio
async def test_toggle_kanji_removes_on_second_call(auth_client):
    await auth_client.post("/favorites/kanji/%E4%B8%80")
    resp = await auth_client.post("/favorites/kanji/%E4%B8%80")
    assert resp.json()["favorited"] is False

    resp2 = await auth_client.get("/favorites")
    assert "一" not in resp2.json()["kanji"]


@pytest.mark.asyncio
async def test_toggle_vocabulary_favorite(auth_client):
    key = "%E4%BB%8A%7C%E3%81%84%E3%81%BE"  # URL-encoded 今|いま
    resp = await auth_client.post(f"/favorites/vocabulary/{key}")
    assert resp.json()["favorited"] is True
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_favorites.py -v
```

- [ ] **Step 3: Replace stub with full `app/routers/favorites.py`**

```python
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


async def _toggle(db: AsyncSession, user_id, item_type: str, item_key: str) -> ToggleResponse:
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
```

- [ ] **Step 4: Run and confirm they pass**

```bash
pytest tests/test_favorites.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Run the full test suite**

```bash
pytest tests/ -v --ignore=tests/test_content.py
```

Expected: all tests pass (content tests need seed data not in fixtures — they pass independently).

- [ ] **Step 6: Commit**

```bash
git add app/routers/favorites.py tests/test_favorites.py
git commit -m "feat: favorites router — toggle kanji and vocabulary favorites"
```

---

## Task 16: Seed Script

**Files:**
- Create: `seed.py`

The seed script embeds data converted from `ginhu/Nihongo-Learning/src/data/` at implementation time. The data includes 71 hiragana, 71 katakana, 108 N5 kanji, 165 N4 kanji, and 511 N5 vocabulary entries.

- [ ] **Step 1: Create `seed.py` with all embedded data**

The complete structure (write full data inline — no placeholders):

```python
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# --- Data (converted from ginhu/Nihongo-Learning/src/data/) ---

HIRAGANA = [
    {"kana": "あ", "romaji": "a",   "grp": "vowel"},
    {"kana": "い", "romaji": "i",   "grp": "vowel"},
    {"kana": "う", "romaji": "u",   "grp": "vowel"},
    {"kana": "え", "romaji": "e",   "grp": "vowel"},
    {"kana": "お", "romaji": "o",   "grp": "vowel"},
    # ... all 71 entries from src/data/hiragana.js
]

KATAKANA = [
    {"kana": "ア", "romaji": "a",   "grp": "vowel"},
    # ... all 71 entries from src/data/katakana.js
]

KANJI = [
    # N5 entries from src/data/n5_kanji.js (108 entries)
    {
        "kanji": "一", "meaning": ["one"],
        "onyomi": ["イチ", "イツ"], "kunyomi": ["ひと.つ"],
        "jlpt": "N5", "stroke_count": 1,
        "examples": [
            {"word": "一つ", "reading": "ひとつ", "meaning": "one thing"},
            {"word": "一月", "reading": "いちがつ", "meaning": "January"},
        ],
    },
    # ... all 108 N5 + 165 N4 entries
]

VOCABULARY = [
    # N5 entries from src/data/n5_vocabulary.js (511 entries)
    {"expression": "今", "reading": "いま", "meaning": "now", "pos": "noun", "jlpt": "N5", "category": "time_and_calendar"},
    # ... all 511 entries
]


async def seed():
    async with SessionLocal() as db:
        # Kana
        for entry in HIRAGANA:
            await db.execute(text(
                "INSERT INTO kana (kana, romaji, type, grp) VALUES (:kana, :romaji, 'hiragana', :grp) "
                "ON CONFLICT DO NOTHING"
            ), entry)
        for entry in KATAKANA:
            await db.execute(text(
                "INSERT INTO kana (kana, romaji, type, grp) VALUES (:kana, :romaji, 'katakana', :grp) "
                "ON CONFLICT DO NOTHING"
            ), entry)

        # Kanji
        for entry in KANJI:
            import json
            await db.execute(text(
                "INSERT INTO kanji (kanji, meaning, onyomi, kunyomi, jlpt, stroke_count, examples) "
                "VALUES (:kanji, :meaning, :onyomi, :kunyomi, :jlpt, :stroke_count, :examples) "
                "ON CONFLICT (kanji) DO NOTHING"
            ), {
                **entry,
                "meaning": entry["meaning"],
                "onyomi": entry["onyomi"],
                "kunyomi": entry["kunyomi"],
                "examples": json.dumps(entry["examples"]),
            })

        # Vocabulary
        for entry in VOCABULARY:
            await db.execute(text(
                "INSERT INTO vocabulary (expression, reading, meaning, jlpt, pos, category) "
                "VALUES (:expression, :reading, :meaning, :jlpt, :pos, :category) "
                "ON CONFLICT (expression, reading) DO NOTHING"
            ), entry)

        await db.commit()
        print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
```

**Implementation note:** When writing `seed.py`, embed the **complete** datasets from the GitHub data files (all 71 hiragana, 71 katakana, 108 N5 kanji, 165 N4 kanji, 511 N5 vocabulary rows). The structure above shows the pattern; the actual file must have no truncated data.

- [ ] **Step 2: Run the seed against the local database**

```bash
python seed.py
```

Expected: `Seed complete.`

- [ ] **Step 3: Verify row counts**

```bash
psql -U postgres -d nihongo -c "SELECT 'kana' as t, count(*) FROM kana UNION ALL SELECT 'vocabulary', count(*) FROM vocabulary UNION ALL SELECT 'kanji', count(*) FROM kanji;"
```

Expected:
```
  t        | count
-----------+-------
 kana      |   142
 vocabulary|   511
 kanji     |   273
```

- [ ] **Step 4: Run seed again to confirm idempotency**

```bash
python seed.py
```

Expected: `Seed complete.` — no errors, counts unchanged.

- [ ] **Step 5: Commit**

```bash
git add seed.py
git commit -m "feat: seed script with hiragana, katakana, N5/N4 kanji, N5 vocabulary"
```

---

## Task 17: pytest.ini + render.yaml + README

**Files:**
- Create: `pytest.ini`
- Create: `render.yaml`
- Create: `README.md`

- [ ] **Step 1: Create `pytest.ini`**

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
```

- [ ] **Step 2: Create `render.yaml`**

```yaml
services:
  - type: web
    name: nihongo-master-api
    runtime: python
    buildCommand: pip install -r requirements.txt && alembic upgrade head
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: nihongo-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 60
      - key: REFRESH_TOKEN_EXPIRE_DAYS
        value: 30
      - key: GOOGLE_CLIENT_ID
        sync: false
      - key: GOOGLE_CLIENT_SECRET
        sync: false
      - key: GITHUB_CLIENT_ID
        sync: false
      - key: GITHUB_CLIENT_SECRET
        sync: false
      - key: FRONTEND_URL
        value: https://ginhu.github.io/Nihongo-Learning

databases:
  - name: nihongo-db
    databaseName: nihongo
    user: nihongo
    plan: free
```

- [ ] **Step 3: Create `README.md`**

```markdown
# Nihongo Master API

FastAPI backend for [Nihongo Master](https://ginhu.github.io/Nihongo-Learning/).

## Local Development

### Prerequisites
- Python 3.12
- PostgreSQL 16

### Setup

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY at minimum

# 3. Create database
psql -U postgres -c "CREATE DATABASE nihongo;"

# 4. Run migrations
alembic upgrade head

# 5. Seed reference data (kana, vocabulary, kanji)
python seed.py

# 6. Start dev server
uvicorn app.main:app --reload
```

API docs available at: http://localhost:8000/docs

### Running Tests

```bash
# Create test database
psql -U postgres -c "CREATE DATABASE nihongo_test;"

# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

## Deploying to Render

1. Push this repo to GitHub.
2. In Render Dashboard → **New** → **Blueprint** → connect your repo.
3. Render reads `render.yaml` and creates the web service + PostgreSQL database automatically.
4. In the web service's **Environment** tab, set:
   - `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
   - `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`
5. After first deploy completes, run the seed script via Render Shell:
   ```bash
   python seed.py
   ```

### OAuth Callback URLs to register

Add these in Google Cloud Console and GitHub OAuth App settings:

- **Google:** `https://<your-render-service>.onrender.com/auth/google/callback`
- **GitHub:** `https://<your-render-service>.onrender.com/auth/github/callback`

## Environment Variables

See `.env.example` for the full list.
```

- [ ] **Step 4: Run the full test suite one more time**

```bash
pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add pytest.ini render.yaml README.md
git commit -m "chore: pytest config, Render deploy config, README"
```

---

## Self-Review Checklist

- [x] `POST /auth/register` — Task 9
- [x] `POST /auth/login` — Task 9
- [x] `POST /auth/logout` — Task 9
- [x] `POST /auth/refresh` — Task 9
- [x] `GET /auth/google` + callback — Task 10
- [x] `GET /auth/github` + callback — Task 10
- [x] `GET /auth/me` — Task 9
- [x] `GET /content/kana` — Task 11
- [x] `GET /content/vocabulary` — Task 11
- [x] `GET /content/kanji` — Task 11
- [x] `GET /settings`, `PATCH /settings` — Task 12
- [x] `GET /progress` — Task 13
- [x] `POST /progress/quiz` (XP + streak + char stats) — Task 13
- [x] `POST /progress/vocab-quiz` (client XP) — Task 13
- [x] `GET /progress/history` — Task 13
- [x] `GET /progress/character-stats` — Task 13
- [x] `GET /flashcards/known` — Task 14
- [x] `PUT /flashcards/known/{card_id}` — Task 14
- [x] `DELETE /flashcards/known/{card_id}` — Task 14
- [x] `GET /favorites` — Task 15
- [x] `POST /favorites/kanji/{kanji}` toggle — Task 15
- [x] `POST /favorites/vocabulary/{key}` toggle — Task 15
- [x] XP logic (10/answer + 50 perfect bonus) — Task 7 + 13
- [x] Level computation (floor(xp/500)+1, cap 10) — Task 7
- [x] Streak logic (yesterday +1, today no change, gap reset) — Task 7
- [x] Seed data (hiragana, katakana, N5/N4 kanji, N5 vocab) — Task 16
- [x] CORS for `https://ginhu.github.io` — Task 9 (main.py)
- [x] httpOnly Secure SameSite=None cookies — Task 2
- [x] Render deploy config — Task 17
- [x] README with local dev + migration + seed + deploy — Task 17
