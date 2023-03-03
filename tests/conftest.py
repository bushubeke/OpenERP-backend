import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from manage import app
from main.db import Base, get_session
from config import TestSettings


@pytest.fixture(scope="session")
def client():
    import asyncio
    settings = TestSettings()
    engine = create_engine(settings.SQLITE_SYNC_URL_PREFIX_TEST, future=True, echo=True)
    async_engine = create_async_engine(settings.SQLITE_ASYNC_URL_PREFIX_TEST, future=True, echo=True)

    session_made = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

    async def get_test_session() -> AsyncSession:
        async with session_made() as session:
            yield session

    def create_all():
        with engine.begin():
            Base.metadata.create_all(engine)

    create_all()

    def drop_tables():
        with engine.begin():
            Base.metadata.drop_all(engine, checkfirst=False)

    app.dependency_overrides[get_session] = get_test_session
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    drop_tables()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
