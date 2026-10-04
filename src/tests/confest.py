# Здесь подготавливается окружение, переменные, ресурсы, состояния для тестирования
# Пока тормозну. Мне нужно переписать логику создания тестовых/продакшн сессий и движка через url
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from src.core.database import create_engine_factory
from src.tests.factory.user_factory import User_Factory


@pytest.fixture
def create_test_engine(TEST_URL):
    test_engine = create_engine_factory(TEST_URL)
    return test_engine

@pytest.fixture
def create_test_session(test_engine:AsyncEngine):
    test_session = async_sessionmaker(test_engine,class_=AsyncSession,expire_on_commit=False)
    return test_session

@pytest.fixture
async def async_client(factory:User_Factory,session:AsyncSession):
    # Factory создает асинхро:нного клиента
    async_client = factory.base_test_user()
    session.add(async_client)
    await session.commit()
    await session.refresh(async_client)
    return async_client
