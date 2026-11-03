# Здесь подготавливается окружение, переменные, ресурсы, состояния для тестирования
from collections.abc import AsyncGenerator  # noqa: F401
import pytest_asyncio,pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from src.core.database import create_engine_factory, get_session
from src.main import app
from src.models.comp_models import BDBase 
from src.tests.factory.user_factory import User_Factory
from src.tests.testdb_settings import TESTDBSettings


@pytest.fixture
def test_url():
    settings = TESTDBSettings() # type: ignore
    assert settings.POSTGRES_DB.startswith("test_")
    return settings.test_db_url

@pytest_asyncio.fixture
async def test_engine(test_url):
    t_engine = create_engine_factory(test_url)
    async with t_engine.begin() as connection:
        await connection.run_sync(BDBase.metadata.create_all)
    yield t_engine
    # dispose закрывает все используемые соеднинения
    await t_engine.dispose()
    
@pytest_asyncio.fixture
async def test_session(test_engine:AsyncEngine):
    TestSession = async_sessionmaker(test_engine,class_=AsyncSession,expire_on_commit=False)
    async with TestSession() as session:
        yield session

@pytest.fixture
def user_factory(test_session):
    return User_Factory(test_session)
# ТОЛЬКО ДЛЯ ТЕСТОВ С БАЗОЙ ДАННЫХ
@pytest_asyncio.fixture
async def test_user(user_factory,test_session:AsyncSession):
    # Factory создает асинхро:нного клиента
    base_test_user = user_factory.base_test_user()
    test_session.add(base_test_user)
    await test_session.commit()
    await test_session.refresh(base_test_user)
    return base_test_user

@pytest_asyncio.fixture
async def client(test_engine:AsyncEngine):
    # создаю генератор сессий
    tengine = async_sessionmaker(test_engine,class_=AsyncSession,expire_on_commit=False)
    # функция перезаписи сессии
    async def override_session():
        async with tengine() as session:
            yield session
    # перезаписываю основную сессию на тестовую 
    app.dependency_overrides[get_session] = override_session
    # стандартное создание клиента
    async with AsyncClient(transport=ASGITransport(app=app),base_url="https://tests") as async_client:
        yield async_client
    app.dependency_overrides.clear()