from collections.abc import AsyncGenerator #noqa
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker #noq
from src.core.db_config import DB_URL
from src.models.comp_models import BDBase,Compliment,User,History #noqa
# добавить отображение ошибок

async_engine = create_async_engine(
    echo=True,
    url = DB_URL,
    pool_size= 10,
    max_overflow=20,
    pool_pre_ping = True
)

async_session = async_sessionmaker(async_engine,expire_on_commit=False)
# Нужно импортировать все модели до Base.metadata.create_all. Без импорта их просто не видят
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BDBase.metadata.create_all)
        

async def reset_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BDBase.metadata.drop_all)
        await conn.run_sync(BDBase.metadata.create_all)

async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        yield session