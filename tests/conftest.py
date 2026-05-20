import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
import os

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/nihongo_test",
)

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
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
async def clean_tables():
    yield
    async with TestSessionLocal() as session:
        await session.execute(text("TRUNCATE users RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE kana, vocabulary, kanji RESTART IDENTITY"))
        await session.commit()


@pytest_asyncio.fixture
async def client():
    from app.main import app
    from app.database import get_db

    async def override_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture
async def db():
    async with TestSessionLocal() as session:
        yield session
