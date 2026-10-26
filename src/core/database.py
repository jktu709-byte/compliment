from collections.abc import AsyncGenerator
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession,AsyncEngine,async_sessionmaker, create_async_engine
from src.core.db_config import db_settings


def create_engine_factory(some_url:URL)->AsyncEngine:
    engine = create_async_engine(
        echo=True,
        url = some_url,
        pool_size= 10,
        max_overflow=20,
        pool_pre_ping = True)
    return engine

db_engine = create_engine_factory(db_settings.db_url)
db_session = async_sessionmaker(db_engine,class_= AsyncSession,expire_on_commit=False)

async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with db_session() as session:
        yield session