#  Используется для декоратора на проверку соединения
from sqlalchemy import text

from src.core.database import db_engine


async def check_db_conn()-> bool:
    try:
        async with db_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception: # noqa: BLE001
        return False