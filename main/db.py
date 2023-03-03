from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import settings

engine = create_engine(settings.SQLITE_SYNC_URL_PREFIX, future=True, echo=True)
asyncengine = create_async_engine(settings.SQLITE_ASYNC_URL_PREFIX, future=True, echo=True)
# engine = create_engine(settings.POSTGRES_SYNC_URL, future=True, echo=True)
# asyncengine=create_async_engine(settings.POSTGRES_ASYNC_URL,future=True, echo=True)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
Base = declarative_base()


async def async_main():
    async with asyncengine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def droptables():
    async with asyncengine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all(engine, checkfirst=False))


sessionmade = sessionmaker(bind=asyncengine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with sessionmade() as session:
        yield session


async def validate(session):
    try:
        # Try to get the underlying session connection, If you can get it, its up
        async with session() as session:
            session.connection()
        return True
    except Exception:
        return False
