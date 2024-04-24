from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

NAME_HOST = "postgresql"

DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@{NAME_HOST}/product_engine"


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
"""
создать разные синглтоны через lru_cache, посмотреть на depends в аргументах dao,  
"""


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
