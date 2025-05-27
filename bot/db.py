from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import POSTGRES_URL

engine = create_async_engine(url=POSTGRES_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper
