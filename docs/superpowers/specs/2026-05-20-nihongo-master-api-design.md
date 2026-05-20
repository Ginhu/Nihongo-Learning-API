# Nihongo Master API — Design Spec
**Date:** 2026-05-20  
**Status:** Approved  
**Deploy target:** Render (Python 3.12 web service + Render-managed PostgreSQL 16)  
**Frontend:** Vue 3 SPA at `https://ginhu.github.io/Nihongo-Learning/`

---

## 1. Architecture & Project Structure

FastAPI application with async SQLAlchemy 2.x (asyncpg driver). All I/O is async. Single Alembic migration creates the full schema. Seed data is embedded in `seed.py` (converted from frontend JS data files at design time).

```
app/
  main.py                  — app factory, CORS middleware, router mounts
  database.py              — async engine + session factory, get_db dependency
  models/
    __init__.py
    user.py                — User, OAuthAccount, UserSettings, UserProgress
    content.py             — Kana, Vocabulary, Kanji
    activity.py            — QuizHistory, CharacterStats, FlashcardKnown, Favorites
  schemas/
    auth.py
    content.py
    settings.py
    progress.py
    flashcards.py
    favorites.py
  routers/
    auth.py
    content.py
    settings.py
    progress.py
    flashcards.py
    favorites.py
  services/
    auth_service.py        — register, login, OAuth upsert, token rotation
    progress_service.py    — XP calc, streak, level, character stats update
  core/
    config.py              — Pydantic BaseSettings, reads .env
    security.py            — JWT encode/decode, bcrypt hash/verify, cookie helpers
  alembic/
    env.py
    versions/
      0001_initial_schema.py
seed.py                    — idempotent seed, data embedded as Python dicts
requirements.txt
.env.example
render.yaml
README.md
```

---

## 2. Tech Stack

| Concern | Library |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.x async |
| DB driver | asyncpg |
| Migrations | Alembic |
| JWT | python-jose[cryptography] |
| Password hashing | passlib[bcrypt] |
| OAuth | authlib |
| Settings | pydantic-settings |
| Server | uvicorn |

---

## 3. Database Schema

### users
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | `gen_random_uuid()` |
| email | text UNIQUE NOT NULL | |
| username | text UNIQUE NOT NULL | |
| password_hash | text NULLABLE | null for OAuth-only accounts |
| created_at | timestamptz | server default now() |
| updated_at | timestamptz | server default now() |

### oauth_accounts
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | cascade delete |
| provider | text | `'google'` or `'github'` |
| provider_user_id | text | |
| UNIQUE | (provider, provider_user_id) | |

### user_settings
| Column | Type | Default |
|---|---|---|
| user_id | UUID PK FK → users | |
| quiz_length | int | 10 |
| romaji_visible | bool | true |
| sound_enabled | bool | true |
| theme | text | `'dark'` |
| language | text | `'en'` |

### user_progress
| Column | Type | Default |
|---|---|---|
| user_id | UUID PK FK → users | |
| xp | int | 0 |
| streak | int | 0 |
| last_played_date | date NULLABLE | |

### quiz_history
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | |
| mode | text | |
| score | int | |
| total | int | |
| xp_gained | int | |
| played_at | timestamptz | server default now() |

### character_stats
| Column | Type | Default |
|---|---|---|
| user_id | UUID | composite PK with char_key |
| char_key | text | composite PK with user_id |
| correct | int | 0 |
| incorrect | int | 0 |

### flashcard_known
| Column | Type | Notes |
|---|---|---|
| user_id | UUID | composite PK with card_id |
| card_id | text | composite PK with user_id |
| known | bool | |

### favorites
| Column | Type | Notes |
|---|---|---|
| user_id | UUID | composite PK (all three) |
| item_type | text | `'kanji'` or `'vocabulary'` |
| item_key | text | kanji char or `expression\|reading` |

### kana
| Column | Type | Notes |
|---|---|---|
| id | serial PK | |
| kana | text | |
| romaji | text | |
| type | text | `'hiragana'` or `'katakana'` |
| grp | text | e.g. `'vowel'`, `'k'`, `'s'` |

### vocabulary
| Column | Type | Notes |
|---|---|---|
| id | serial PK | |
| expression | text | |
| reading | text | |
| meaning | text | |
| meaning_pt | text NULLABLE | |
| jlpt | text | |
| pos | text NULLABLE | |
| category | text NULLABLE | |
| UNIQUE | (expression, reading) | |

### kanji
| Column | Type | Notes |
|---|---|---|
| id | serial PK | |
| kanji | text UNIQUE | |
| meaning | text[] | PostgreSQL array |
| meaning_pt | text[] NULLABLE | |
| onyomi | text[] | |
| kunyomi | text[] | |
| jlpt | text | |
| stroke_count | int | |
| examples | jsonb | |

---

## 4. Seed Data

`seed.py` embeds data converted from the frontend repo (`ginhu/Nihongo-Learning`) at design time:

| Source file | Table | Rows |
|---|---|---|
| `src/data/hiragana.js` | kana | 71 |
| `src/data/katakana.js` | kana | 71 |
| `src/data/n5_kanji.js` | kanji | 108 |
| `src/data/n4_kanji.js` | kanji | 165 |
| `src/data/n5_vocabulary.js` | vocabulary | 511 |

**Mapping:**
- `group` → `grp`; `type` derived from source file (`'hiragana'`/`'katakana'`)
- `strokeCount` → `stroke_count`
- `meaning[]` stored as PostgreSQL text array
- `examples[]` stored as jsonb
- `romaji` on vocabulary — dropped (not in schema)
- `category` on kanji — dropped (not in schema)
- `meaning_pt` — null (no Portuguese translations in source data)

Idempotent via `INSERT ... ON CONFLICT DO NOTHING`.

---

## 5. Auth & Security

### JWT Cookies
- **`access_token`**: 60-minute HTTPOnly Secure SameSite=None cookie
- **`refresh_token`**: 30-day HTTPOnly Secure SameSite=None cookie
- `SameSite=None; Secure` is required for cross-origin cookie delivery from GitHub Pages to Render
- `POST /auth/refresh`: reads refresh cookie, issues new access token
- `POST /auth/logout`: clears both cookies (sets expired)

### Password Auth
- bcrypt via `passlib[bcrypt]`
- `password_hash` is nullable — OAuth-only accounts have no password

### OAuth Flow (Google + GitHub)
1. `GET /auth/{provider}` — generate signed `state` JWT (10-min TTL), store in short-lived cookie, redirect to provider
2. `GET /auth/{provider}/callback` — validate state cookie, exchange code for tokens, fetch user profile
3. Upsert: if OAuth email matches existing `users.email` → link account; else create new user
4. Create `user_settings` + `user_progress` rows if new user
5. Set JWT cookies, redirect to `https://ginhu.github.io/Nihongo-Learning/#/login?status=success`

### Auth Dependency
`get_current_user` reads `access_token` cookie, decodes JWT, loads user from DB. All protected routes use `Depends(get_current_user)`.

### CORS
```python
CORSMiddleware(
    allow_origins=["https://ginhu.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 6. API Endpoints

### Auth (`/auth`)
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | — | email+password registration |
| POST | `/auth/login` | — | email+password login, sets cookies |
| POST | `/auth/logout` | — | clears cookies |
| POST | `/auth/refresh` | cookie | rotate access token |
| GET | `/auth/google` | — | redirect to Google OAuth |
| GET | `/auth/google/callback` | — | OAuth callback, sets cookies, redirect |
| GET | `/auth/github` | — | redirect to GitHub OAuth |
| GET | `/auth/github/callback` | — | OAuth callback, sets cookies, redirect |
| GET | `/auth/me` | cookie | returns current user |

### Content (`/content`) — public, no auth
| Method | Path | Query params |
|---|---|---|
| GET | `/content/kana` | `?type=hiragana\|katakana` |
| GET | `/content/vocabulary` | `?jlpt=N5&lang=en\|pt&category=` |
| GET | `/content/kanji` | `?jlpt=N5\|N4&lang=en\|pt` |

`lang` param selects `meaning` (en) vs `meaning_pt` (pt) in the response body. When `lang=pt` and `meaning_pt` is null (all seed data), fall back to `meaning`.

### Settings (`/settings`) — auth required
| Method | Path | Description |
|---|---|---|
| GET | `/settings` | returns user settings |
| PATCH | `/settings` | partial update |

### Progress (`/progress`) — auth required
| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/progress` | — | xp, streak, level, last_played_date |
| POST | `/progress/quiz` | `{mode, score, total, answers:[{char_key, was_correct}]}` | `{xp_gained, new_level}` |
| POST | `/progress/vocab-quiz` | `{mode, score, total, xp_total}` | `{xp_gained, new_level}` |
| GET | `/progress/history` | `?mode=` | list of quiz_history rows |
| GET | `/progress/character-stats` | — | all character_stats for user |

### Flashcards (`/flashcards`) — auth required
| Method | Path | Description |
|---|---|---|
| GET | `/flashcards/known` | all known flashcard IDs |
| PUT | `/flashcards/known/{card_id}` | mark card as known |
| DELETE | `/flashcards/known/{card_id}` | remove known mark |

### Favorites (`/favorites`) — auth required
| Method | Path | Description |
|---|---|---|
| GET | `/favorites` | all favorites grouped by type |
| POST | `/favorites/kanji/{kanji}` | toggle kanji favorite |
| POST | `/favorites/vocabulary/{key}` | toggle vocab favorite (`expression\|reading`) |

---

## 7. XP & Progress Logic

Implemented in `progress_service.py`:

```
# POST /progress/quiz
correct_count = sum(1 for a in answers if a.was_correct)
xp_gained = correct_count * 10 + (50 if score == total else 0)
user_progress.xp += xp_gained  # XP is unbounded; only level display is capped

old_level = min(floor(prev_xp / 500) + 1, 10)
new_level = min(floor(new_xp / 500) + 1, 10)

# streak
today = date.today()
if last_played == today:
    pass  # no change
elif last_played == today - timedelta(days=1):
    streak += 1
else:
    streak = 1
last_played = today

# upsert character_stats per answer
INSERT INTO character_stats (user_id, char_key, correct, incorrect)
VALUES (...) ON CONFLICT (user_id, char_key) DO UPDATE
  SET correct = correct + excluded.correct,
      incorrect = incorrect + excluded.incorrect

return { xp_gained, new_level: new_level if new_level > old_level else None }
```

```
# POST /progress/vocab-quiz
xp_gained = xp_total  # client-provided, trusted as-is per spec
# same streak + level logic, no character_stats update
```

---

## 8. Error Handling

| Scenario | HTTP status |
|---|---|
| Invalid/expired token | 401 |
| Duplicate email on register | 409 |
| Resource not found | 404 |
| Validation error | 422 (automatic) |
| OAuth state mismatch | 400 |

All errors use FastAPI's default `{"detail": "..."}` JSON shape.

---

## 9. Deployment (Render)

`render.yaml` defines:
- **Web service**: Python 3.12, `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Build command**: `pip install -r requirements.txt && alembic upgrade head`
- **PostgreSQL 16** managed database, `DATABASE_URL` injected automatically

All secrets set via Render dashboard environment variables (see `.env.example`).

---

## 10. Environment Variables

```
DATABASE_URL=postgresql+asyncpg://...
SECRET_KEY=<random 32-byte hex>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
FRONTEND_URL=https://ginhu.github.io/Nihongo-Learning
```
