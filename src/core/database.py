# добавить отображение ошибок
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker #noqa
from src.core.config import DB_URL
from src.models.comp_models import Base


async_engine = create_async_engine(
    echo=True,
    url = DB_URL,
    pool_size= 10,
    max_overflow=20,
    pool_pre_ping = True
)

async_session = async_sessionmaker(async_engine,expire_on_commit=False)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True

async def reset_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True

async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        yield session