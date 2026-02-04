from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker #noqa
from src.core.config import DB_URL



async_engine = create_async_engine(
    echo=True,
    url = DB_URL,
    pool_size= 10,
    max_overflow=20
)

async_session = async_sessionmaker(async_engine)