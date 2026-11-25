from datetime import UTC, datetime, timedelta

import pytest 
from httpx import AsyncClient
from src.auth.tokens import token_helper
from src.models.comp_models import EmailVerificationToken, User
from src.users.repository import UserRepository
from src.users.service import UserService

@pytest.fixture
def user_service(test_session):
    return UserService(repo=UserRepository(test_session))

@pytest.mark.asyncio
async def test_register(client:AsyncClient,user_service,caplog):
    caplog.set_level("INFO", logger="sqlalchemy.engine.Engine")
    response = await client.post(url="users/register",
        json={
            "name":"John",
            "email":"john123@example.com",
            "gender":"male",
            "password":"exapmlepassword123"}
    )
    assert response.status_code == 201
    assert set(response.json()) == {"id", "name", "created_at"}
    user = await user_service.get_email("john123@example.com")
    assert user is not None
    assert user.name == "John"
    assert user.email_verified_at is None
    assert user.password_hash != "exapmlepassword123"
    assert "SQL parameters hidden" in caplog.text
    assert not any(user.password_hash in message for message in caplog.messages)


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


@pytest.mark.asyncio
@pytest.mark.parametrize("expired", [False, True], ids=["valid-and-reused", "expired"])
async def test_confirm_email(client, test_session, email_task_mock, expired):
    registration = await client.post("/users/register", json={
        "name": "Reader", "email": "reader@example.com",
        "gender": "neutral", "password": "password123",
    })
    assert registration.status_code == 201, registration.text
    email_task_mock.assert_called_once()
    message = email_task_mock.call_args.kwargs
    assert message["to_email"] == "reader@example.com"
    raw_token = message["body"]
    user_id = registration.json()["id"]
    token = await test_session.get(EmailVerificationToken, user_id)
    assert token.token_hash == token_helper.hash_token(raw_token)
    assert token.token_hash != raw_token
    if expired:
        token.expires_at = datetime.now(UTC) - timedelta(seconds=1)
        await test_session.commit()

    response = await client.post("/users/confirm_email", json={"token": raw_token})
    assert response.status_code == (400 if expired else 204), response.text
    test_session.expire_all()
    user = await test_session.get(User, user_id)
    if expired:
        assert user.email_verified_at is None
        assert response.json()["code"] == "INVALID_EMAIL_VERIFICATION_TOKEN"
    else:
        assert response.content == b""
        assert user.email_verified_at is not None
        assert await test_session.get(EmailVerificationToken, user_id) is None
        repeated = await client.post("/users/confirm_email", json={"token": raw_token})
        assert repeated.status_code == 400
        assert repeated.json()["code"] == "INVALID_EMAIL_VERIFICATION_TOKEN"


@pytest.mark.asyncio
async def test_confirm_email_rejects_unknown_token(client):
    response = await client.post("/users/confirm_email", json={"token": "unknown-token"})
    assert response.status_code == 400, response.text
    assert response.json()["code"] == "INVALID_EMAIL_VERIFICATION_TOKEN"
