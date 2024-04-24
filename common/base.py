from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import *
from aiokafka import AIOKafkaProducer

import os


Base = declarative_base()
async def ret_async_session(db_connect: str):
    engine = create_async_engine(db_connect, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return async_session


async def get_session() -> AsyncSession:
    async with (await ret_async_session(os.getenv("DB_CONNECT")))() as session:
        yield session

async def get_producer() -> AIOKafkaProducer:
    aioproducer = AIOKafkaProducer(bootstrap_servers=KAFKA_INSTANCE)
    yield aioproducer
