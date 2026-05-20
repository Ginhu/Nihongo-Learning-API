import ssl
from collections.abc import AsyncGenerator
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


def build_engine(database_url: str):
    parsed = urlparse(database_url)
    params = parse_qs(parsed.query, keep_blank_values=True)

    connect_args = {}
    needs_ssl = bool(params.pop("ssl", None) or params.pop("sslmode", None))
    params.pop("channel_binding", None)

    if needs_ssl:
        ctx = ssl.create_default_context()
        connect_args["ssl"] = ctx

    clean_query = urlencode({k: v[0] for k, v in params.items()})
    clean_url = urlunparse(parsed._replace(query=clean_query))
    return create_async_engine(clean_url, connect_args=connect_args, echo=False)


engine = build_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
