import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "fc@example.com", "username": "fcuser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_known_starts_empty(auth_client):
    resp = await auth_client.get("/flashcards/known")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_put_marks_card_known(auth_client):
    resp = await auth_client.put("/flashcards/known/card-abc")
    assert resp.status_code == 200
    assert resp.json()["known"] is True

    resp2 = await auth_client.get("/flashcards/known")
    assert any(c["card_id"] == "card-abc" for c in resp2.json())


@pytest.mark.asyncio
async def test_delete_removes_card(auth_client):
    await auth_client.put("/flashcards/known/card-del")
    resp = await auth_client.delete("/flashcards/known/card-del")
    assert resp.status_code == 204

    resp2 = await auth_client.get("/flashcards/known")
    assert not any(c["card_id"] == "card-del" for c in resp2.json())


@pytest.mark.asyncio
async def test_delete_nonexistent_returns_404(auth_client):
    resp = await auth_client.delete("/flashcards/known/does-not-exist")
    assert resp.status_code == 404
