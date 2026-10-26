#  Используется для декоратора на проверку соединения
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.core.database import db_engine

@pytest.mark.asyncio
async def test_db_conn(engine:AsyncEngine = db_engine):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {True:"OK"}
    except Exception as e:  # noqa: BLE001
        return print(e.__class__)