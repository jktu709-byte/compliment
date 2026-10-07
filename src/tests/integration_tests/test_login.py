from httpx import AsyncClient

from src.auth.auth_service import AuthService
from src.models.comp_models import User


async def test_login(client:AsyncClient,service:AuthService,user:User):
    # отправляю запрос
    res = await client.post(
        "/login/jwt",
        json={
            "email":user.email,
            "password":"random_password"
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
    