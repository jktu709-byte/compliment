import json
from io import BytesIO

import pytest
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.compliments.repository import ComplimentRepository
from src.compliments.service import COMPLIMENT_KEY, ComplimentService
from src.models.comp_models import Gender
from src.tests.factory.complmnt_factory import Complmnt_Factory
from src.users.repository import UserRepository


@pytest.fixture
def complmnt_factory(test_session:AsyncSession) -> Complmnt_Factory:
    return Complmnt_Factory(test_session)
    
@pytest.mark.asyncio 
async def test_add_data(complmnt_factory):
    res = await complmnt_factory.create_complmnt()
    assert  res.title == "test_title"
    assert res.gender == Gender.neutral
    assert res.point == "test_point"
    return res


@pytest.mark.asyncio
async def test_import_invalidates_cached_compliments(
    complmnt_factory, test_session: AsyncSession, client, test_cache
):
    # Фабрика создаёт первый комплимент и сохраняет его
    await complmnt_factory.create_complmnt()
    await test_session.commit()
    # возвращает список, записывает в кэш
    first_response = await client.get("/compliments/data/all")
    # проверка на успех и соответствие
    assert first_response.status_code == 200, first_response.text
    assert [item["title"] for item in first_response.json()["compliments"]] == ["test_title"]
    # проверка, что кэш записался и время пошло
    assert COMPLIMENT_KEY in test_cache.data
    assert COMPLIMENT_KEY in test_cache.ttl
    # Тест создаёт service с той же тестовой БД и тем же объектом кэша.
    service = ComplimentService(
        repo=ComplimentRepository(test_session),
        u_repo=UserRepository(test_session),
        cache=test_cache,
    )
    # второй комплимент
    payload = {"compliments": [{"title": "second_title", "gender": "neutral", "point": "second_point"}]}
    # изображает загруженный JSON-файл со вторым комплиментом
    with BytesIO(json.dumps(payload).encode()) as upload_stream:
        await service.input_data_from_file(UploadFile(file=upload_stream, filename="compliments.json"))
    # проверка на отстутсвие
    assert COMPLIMENT_KEY not in test_cache.data
    assert COMPLIMENT_KEY not in test_cache.ttl
    # второй запрос делает то же самое, что и первый
    second_response = await client.get("/compliments/data/all")
    # проверка второго запроса
    assert second_response.status_code == 200, second_response.text
    assert {item["title"] for item in second_response.json()["compliments"]} == {
        "test_title", "second_title"
    }
