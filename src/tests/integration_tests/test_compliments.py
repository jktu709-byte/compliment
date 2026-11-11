import pytest
import pytest_asyncio

from src.models.comp_models import Compliment, Gender


@pytest_asyncio.fixture
async def reader_id(client):
    response = await client.post(
        "/users/register",
        json={
            "name": "Reader",
            "email": "reader@example.com",
            "gender": "neutral",
            "password": "password123",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


@pytest.mark.asyncio
async def test_list_compliments_when_empty(client):
    response = await client.get("/compliments/data/all")

    assert response.status_code == 404, response.text
    assert response.json()["code"] == "COMPLIMENT_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_compliments(client, test_session):
    compliment = Compliment(title="You are kind", gender=Gender.neutral, point="Kindness")
    test_session.add(compliment)
    await test_session.commit()

    response = await client.get("/compliments/data/all")

    assert response.status_code == 200, response.text
    compliments = response.json()["compliments"]
    assert len(compliments) == 1
    assert compliments[0]["id"] == compliment.id
    assert compliments[0]["title"] == "You are kind"
    assert compliments[0]["gender"] == "neutral"
    assert compliments[0]["point"] == "Kindness"
    assert compliments[0]["created_at"]


@pytest.mark.asyncio
async def test_random_compliment_when_empty(client, reader_id):
    response = await client.get(f"/compliments/data/random/{reader_id}")

    assert response.status_code == 404, response.text
    assert response.json()["code"] == "COMPLIMENT_NOT_FOUND"


@pytest.mark.asyncio
async def test_random_compliment_is_saved_in_history(client, test_session, reader_id):
    compliment = Compliment(title="You are kind", gender=Gender.neutral, point=None)
    test_session.add(compliment)
    await test_session.commit()

    response = await client.get(f"/compliments/data/random/{reader_id}")
    assert response.status_code == 200, response.text
    assert response.json()["id"] == compliment.id

    history = await client.get(f"/compliments/history/{reader_id}")
    assert history.status_code == 200, history.text
    assert [item["id"] for item in history.json()] == [compliment.id]


@pytest.mark.asyncio
async def test_update_missing_compliment(client):
    response = await client.put("/compliments/data/999999")

    assert response.status_code == 404, response.text
