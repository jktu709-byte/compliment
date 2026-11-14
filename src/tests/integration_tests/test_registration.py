import pytest 
from httpx import AsyncClient
from src.users.repository import UserRepository
from src.users.service import UserService

@pytest.fixture
def user_service(test_session):
    return UserService(repo=UserRepository(test_session))

@pytest.mark.asyncio
async def test_register(client:AsyncClient,user_service):
    response = await client.post(url="users/register",
        json={
            "name":"John",
            "email":"john123@example.com",
            "gender":"male",
            "password":"exapmlepassword123"}
    )
    assert response.status_code == 201
    user = await user_service.get_email("john123@example.com")
    assert user is not None
    assert user.name == "John"
    assert user.password_hash != "exapmlepassword123"


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(client: AsyncClient):
    payload = {
        "name": "John",
        "email": "duplicate@example.com",
        "gender": "male",
        "password": "password123",
    }
    first = await client.post("/users/register", json=payload)
    assert first.status_code == 201, first.text

    duplicate = await client.post("/users/register", json=payload)
    assert duplicate.status_code == 400, duplicate.text
    assert duplicate.json()["detail"] == "User already exist"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"name": "John", "email": "invalid", "gender": "male", "password": "password123"},
        {"name": "John", "email": "john@example.com", "gender": "other", "password": "password123"},
        {"name": "John", "email": "john@example.com", "gender": "male"},
    ],
)
async def test_register_rejects_invalid_payload(client: AsyncClient, payload):
    response = await client.post("/users/register", json=payload)

    assert response.status_code == 422, response.text
