from httpx import ASGITransport, AsyncClient

from src.api.repository import UserRepository
from src.main import app


async def test_register(service:UserRepository):
    async with AsyncClient(transport=ASGITransport(app=app),base_url="https://test") as ac:
        response = await ac.post(
            "users/register",
            json={
                "name":"John",
                "email":"john@example.com",
                "gender":"male",
                "password":"exapmlepassword123"
            }
        )
        assert response.status_code == 200
        user = await service.get_user_by_email(email="john@example.com")
        assert user is not None
        assert user.name == "John"
        assert user.password_hash != "exapmlepassword123"