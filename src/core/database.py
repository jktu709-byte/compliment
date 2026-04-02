from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker #noqa
from src.core.config import DB_URL
from src.api.crud import ComplimentRepository


async_engine = create_async_engine(
    echo=True,
    url = DB_URL,
    pool_size= 10,
    max_overflow=20,
    pool_pre_ping = True
)

async_session = async_sessionmaker(async_engine,expire_on_commit=False)

async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        yield session

async def depends_session(session:AsyncSession = Depends(get_session))->ComplimentRepository:
    return ComplimentRepository(session)