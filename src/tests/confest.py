# Здесь подготавливается окружение, переменные, ресурсы, состояния для тестирования
# Пока тормозну. Мне нужно переписать логику создания тестовых/продакшн сессий и движка через url
from collections.abc import AsyncGenerator  # noqa: F401

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from src.core.database import create_engine_factory
from src.main import app
from src.models.comp_models import BDBase
from src.tests.factory.user_factory import User_Factory


@pytest.fixture
async def create_test_engine(TEST_URL):
    test_engine = create_engine_factory(TEST_URL)
    async with test_engine.begin() as connection:
        await connection.run_sync(BDBase.metadata.create_all)

@pytest.fixture
async def create_test_session(test_engine:AsyncEngine):
    TestSession = async_sessionmaker(test_engine,class_=AsyncSession,expire_on_commit=False)

    async with TestSession() as session:
        yield session

@pytest.fixture
async def async_base_client(factory:User_Factory,session:AsyncSession):
    # Factory создает асинхро:нного клиента
    test_user = factory.base_test_user()
    session.add(test_user)
    await session.commit()
    await session.refresh(test_user)
    return test_user

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="https://tests") as async_client:
        yield async_client
        