from src.models.comp_models import User
import pytest
import pytest_asyncio

@pytest.fixture
def user():
    return User

@pytest_asyncio.fixture
async def registered_user(client):
    data = {
        "email": "test@example.com",
        "password":"exapmlepassword123",
        "name": "Test",
        "gender":"male"
        }
    r = await client.post("/users/register", json=data)
    assert r.status_code == 201, r.text
    return data

@pytest.mark.asyncio
async def test_login(client,registered_user):
    # отправляю запрос
    res = await client.post(
        "/auth/login/jwt",
        json=registered_user
    )
    # операция прошла успешно
    assert res.status_code == 200
    # парсит ответ в json формат и проверяет наличие данных
    data = res.json()
    assert data["access_token"]
    assert data["refresh_token"]
    # проверка что куки сохранились
    assert res.cookies.get("access_token")
    assert res.cookies.get("refresh_token")
    