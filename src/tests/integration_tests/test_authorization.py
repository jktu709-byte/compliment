import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def registered_user(client):
    credentials = {
        "name": "Authorization Test",
        "email": "authorization@example.com",
        "gender": "neutral",
        "password": "correct-password-123",
    }
    response = await client.post("/users/register", json=credentials)
    assert response.status_code == 201, response.text
    return credentials


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("missing@example.com", "correct-password-123"),
        ("authorization@example.com", "wrong-password"),
    ],
)
async def test_login_rejects_invalid_credentials(client, registered_user, email, password):
    response = await client.post(
        "/auth/login/jwt",
        json={"name": registered_user["name"], "email": email, "password": password},
    )

    assert response.status_code == 401, response.text
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies


@pytest.mark.asyncio
async def test_refresh_rotates_token_and_rejects_reuse(client, registered_user):
    login = await client.post("/auth/login/jwt", json=registered_user)
    assert login.status_code == 200, login.text
    old_refresh = login.json()["refresh_token"]

    refreshed = await client.request(
        "GET", "/auth/tokens/refresh", json={"refresh_token": old_refresh}
    )
    assert refreshed.status_code == 200, refreshed.text
    assert refreshed.json()["access_token"]
    assert refreshed.json()["refresh_token"] != old_refresh
    assert refreshed.cookies.get("refresh_token") == refreshed.json()["refresh_token"]

    reused = await client.request(
        "GET", "/auth/tokens/refresh", json={"refresh_token": old_refresh}
    )
    assert reused.status_code == 401, reused.text


@pytest.mark.asyncio
async def test_refresh_rejects_unknown_token(client):
    response = await client.request(
        "GET", "/auth/tokens/refresh", json={"refresh_token": "unknown-token"}
    )

    assert response.status_code == 401, response.text
