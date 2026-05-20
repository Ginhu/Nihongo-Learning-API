import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "fav@example.com", "username": "favuser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_favorites_start_empty(auth_client):
    resp = await auth_client.get("/favorites")
    assert resp.status_code == 200
    assert resp.json() == {"kanji": [], "vocabulary": []}


@pytest.mark.asyncio
async def test_toggle_kanji_adds_favorite(auth_client):
    resp = await auth_client.post("/favorites/kanji/%E4%B8%80")  # URL-encoded 一
    assert resp.status_code == 200
    assert resp.json()["favorited"] is True

    resp2 = await auth_client.get("/favorites")
    assert "一" in resp2.json()["kanji"]


@pytest.mark.asyncio
async def test_toggle_kanji_removes_on_second_call(auth_client):
    await auth_client.post("/favorites/kanji/%E4%B8%80")
    resp = await auth_client.post("/favorites/kanji/%E4%B8%80")
    assert resp.json()["favorited"] is False

    resp2 = await auth_client.get("/favorites")
    assert "一" not in resp2.json()["kanji"]


@pytest.mark.asyncio
async def test_toggle_vocabulary_favorite(auth_client):
    key = "%E4%BB%8A%7C%E3%81%84%E3%81%BE"  # URL-encoded 今|いま
    resp = await auth_client.post(f"/favorites/vocabulary/{key}")
    assert resp.json()["favorited"] is True
