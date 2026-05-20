import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "s@example.com", "username": "suser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_get_settings_returns_defaults(auth_client):
    resp = await auth_client.get("/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["quiz_length"] == 10
    assert data["theme"] == "dark"
    assert data["language"] == "en"


@pytest.mark.asyncio
async def test_patch_settings(auth_client):
    resp = await auth_client.patch("/settings", json={"theme": "light", "quiz_length": 20})
    assert resp.status_code == 200
    data = resp.json()
    assert data["theme"] == "light"
    assert data["quiz_length"] == 20
    assert data["language"] == "en"  # unchanged


@pytest.mark.asyncio
async def test_settings_requires_auth(client):
    resp = await client.get("/settings")
    assert resp.status_code == 401
