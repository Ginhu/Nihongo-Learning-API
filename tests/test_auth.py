import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_register_creates_user(client):
    resp = await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "secret123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "access_token" in resp.cookies


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client):
    body = {"email": "dup@example.com", "username": "user1", "password": "pass"}
    await client.post("/auth/register", json=body)
    resp = await client.post("/auth/register", json={**body, "username": "user2"})
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_user(client):
    await client.post("/auth/register", json={
        "email": "login@example.com", "username": "loginuser", "password": "pass123",
    })
    resp = await client.post("/auth/login", json={
        "email": "login@example.com", "password": "pass123",
    })
    assert resp.status_code == 200
    assert resp.json()["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(client):
    await client.post("/auth/register", json={
        "email": "wp@example.com", "username": "wpuser", "password": "correct",
    })
    resp = await client.post("/auth/login", json={"email": "wp@example.com", "password": "wrong"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_current_user(client):
    await client.post("/auth/register", json={
        "email": "me@example.com", "username": "meuser", "password": "pass",
    })
    resp = await client.get("/auth/me")
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_logout_clears_cookies(client):
    await client.post("/auth/register", json={
        "email": "lo@example.com", "username": "louser", "password": "pass",
    })
    resp = await client.post("/auth/logout")
    assert resp.status_code == 200
    resp2 = await client.get("/auth/me")
    assert resp2.status_code == 401
