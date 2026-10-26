import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

@pytest.mark.asyncio
async def test_engine_conn(test_engine:AsyncEngine):
    async with test_engine.begin() as conn:
        res = await conn.execute(text("SELECT 1"))
        assert res.scalar_one() == 1
         