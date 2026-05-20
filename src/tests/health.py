#  Используется для декоратора на проверку соединения
from sqlalchemy import text
from src.core.database import async_engine

async def check_db_conn()-> bool:
    try:
        async with async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False