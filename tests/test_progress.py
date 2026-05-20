import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "email": "p@example.com", "username": "puser", "password": "pass",
    })
    return client


@pytest.mark.asyncio
async def test_get_progress_initial(auth_client):
    resp = await auth_client.get("/progress")
    assert resp.status_code == 200
    data = resp.json()
    assert data["xp"] == 0
    assert data["streak"] == 0
    assert data["level"] == 1


@pytest.mark.asyncio
async def test_submit_quiz_updates_xp(auth_client):
    resp = await auth_client.post("/progress/quiz", json={
        "mode": "hiragana",
        "score": 3,
        "total": 3,
        "answers": [
            {"char_key": "あ", "was_correct": True},
            {"char_key": "い", "was_correct": True},
            {"char_key": "う", "was_correct": True},
        ],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["xp_gained"] == 80  # 3*10 + 50 perfect bonus

    progress = await auth_client.get("/progress")
    assert progress.json()["xp"] == 80


@pytest.mark.asyncio
async def test_submit_quiz_level_up(auth_client):
    for _ in range(6):
        await auth_client.post("/progress/quiz", json={
            "mode": "hiragana", "score": 10, "total": 10,
            "answers": [{"char_key": f"k{i}", "was_correct": True} for i in range(10)],
        })
    resp = await auth_client.post("/progress/quiz", json={
        "mode": "hiragana", "score": 10, "total": 10,
        "answers": [{"char_key": f"k{i}", "was_correct": True} for i in range(10)],
    })
    assert resp.json()["new_level"] is not None


@pytest.mark.asyncio
async def test_submit_vocab_quiz(auth_client):
    resp = await auth_client.post("/progress/vocab-quiz", json={
        "mode": "vocab", "score": 5, "total": 10, "xp_total": 50,
    })
    assert resp.status_code == 200
    assert resp.json()["xp_gained"] == 50


@pytest.mark.asyncio
async def test_get_history(auth_client):
    await auth_client.post("/progress/quiz", json={
        "mode": "katakana", "score": 1, "total": 5,
        "answers": [{"char_key": "ア", "was_correct": True}],
    })
    resp = await auth_client.get("/progress/history")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_get_character_stats(auth_client):
    await auth_client.post("/progress/quiz", json={
        "mode": "hiragana", "score": 1, "total": 1,
        "answers": [{"char_key": "あ", "was_correct": True}],
    })
    resp = await auth_client.get("/progress/character-stats")
    assert resp.status_code == 200
    stats = resp.json()
    assert any(s["char_key"] == "あ" and s["correct"] == 1 for s in stats)
