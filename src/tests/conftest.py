# Здесь подготавливается окружение, переменные, ресурсы, состояния для тестирования
import os
import subprocess
import sys  
import pytest_asyncio,pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
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
from dotenv import dotenv_values

@pytest.fixture(scope="session")
def test_url():
    settings = TESTDBSettings() # type: ignore
    assert settings.POSTGRES_DB.startswith("test_")
    return settings.test_db_url
# прописать alembic upgrade head, вместо колхозного create_all
@pytest_asyncio.fixture
async def test_engine(test_url,migrated_db):
    t_engine = create_engine_factory(test_url)
    yield t_engine
    tables = ", ".join(f'"{t.name}"' for t in BDBase.metadata.sorted_tables)
    async with t_engine.begin() as conn:
        await conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    # dispose закрывает все используемые соеднинения
    await t_engine.dispose()
# выполняет инициализацию бд вместо колхозного create_all
@pytest.fixture
def migrated_db(test_url):
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        env={**dotenv_values("tests.env"), **os.environ}, # type: ignore
        check=True,
    ) # type: ignore
    yield
    
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
