from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session


@pytest.fixture
async def get_test_session() -> AsyncGenerator[AsyncSession|None]:
    async with async_session() as session:
        yield session
        await session.rollback()