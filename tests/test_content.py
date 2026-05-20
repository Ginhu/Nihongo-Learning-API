import pytest
import pytest_asyncio
from app.models.content import Kana, Vocabulary, Kanji


@pytest_asyncio.fixture(autouse=True)
async def seed_content(db):
    db.add(Kana(kana="あ", romaji="a", type="hiragana", grp="vowel"))
    db.add(Kana(kana="ア", romaji="a", type="katakana", grp="vowel"))
    db.add(Vocabulary(expression="今", reading="いま", meaning="now", jlpt="N5", category="time"))
    db.add(Vocabulary(expression="水", reading="みず", meaning="water", meaning_pt="água", jlpt="N5", category="nature"))
    db.add(Kanji(
        kanji="一", meaning=["one"], onyomi=["イチ"], kunyomi=["ひと.つ"],
        jlpt="N5", stroke_count=1, examples=[]
    ))
    await db.commit()


@pytest.mark.asyncio
async def test_get_all_kana(client):
    resp = await client.get("/content/kana")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_kana_filtered_by_type(client):
    resp = await client.get("/content/kana?type=hiragana")
    assert resp.status_code == 200
    assert all(k["type"] == "hiragana" for k in resp.json())


@pytest.mark.asyncio
async def test_get_vocabulary(client):
    resp = await client.get("/content/vocabulary?jlpt=N5")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_vocabulary_lang_pt_fallback(client):
    resp = await client.get("/content/vocabulary?lang=pt")
    data = resp.json()
    agua = next(v for v in data if v["expression"] == "水")
    ima = next(v for v in data if v["expression"] == "今")
    assert agua["meaning"] == "água"
    assert ima["meaning"] == "now"  # fallback since meaning_pt is null


@pytest.mark.asyncio
async def test_get_kanji(client):
    resp = await client.get("/content/kanji?jlpt=N5")
    assert resp.status_code == 200
    assert resp.json()[0]["kanji"] == "一"
