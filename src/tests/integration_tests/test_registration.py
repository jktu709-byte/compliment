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