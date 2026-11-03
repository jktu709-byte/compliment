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
    assert r.status_code == 200, r.text
    return data
@pytest.mark.asyncio
async def test_login(registered_user):
    # отправляю запрос
    res = await registered_user.post(
        "/login/jwt",
        json={
            "name": "Test",
            "email": "test@example.com",
            "gender":"male",
            "password":"exapmlepassword123"
            }
    )
    # операция прошла успешно
    assert res.status_code == 200
    # парсит ответ в json формат и проверяет наличие данных
    data = res.json()
    assert data["refersh_token"]
    assert data["refersh_token"]
    # проверка что куки сохранились
    assert res.cookies.get("acces_token")
    assert res.cookies.get("refresh_token")
    