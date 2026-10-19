import pytest #noqa
from httpx import AsyncClient
from src.user.repository import UserRepository


async def test_register(client:AsyncClient,service:UserRepository):
    response = await client.post(
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