from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.db_config import DB_URL
from src.models.comp_models import BDBase

# добавить отображение ошибок

def create_engine_factory(some_url:str):
    engine = create_async_engine(
        echo=True,
        url = some_url,
        pool_size= 10,
        max_overflow=20,
        pool_pre_ping = True
    )
    return engine
db_engine = create_engine_factory(DB_URL)
db_session = async_sessionmaker(db_engine,class_= AsyncSession,expire_on_commit=False)
# Нужно импортировать все модели до Base.metadata.create_all. Без импорта их просто не видят
async def init_db():
    async with db_engine.begin() as conn:
        await conn.run_sync(BDBase.metadata.create_all)
        
async def reset_db():
    async with db_engine.begin() as conn:
        await conn.run_sync(BDBase.metadata.drop_all)
        await conn.run_sync(BDBase.metadata.create_all)

async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with db_session() as session:
        yield session