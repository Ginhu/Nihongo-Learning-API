# Nihongo Master API

FastAPI backend for [Nihongo Master](https://ginhu.github.io/Nihongo-Learning/).

## Local Development

### Prerequisites
- Python 3.12
- PostgreSQL 16

### Setup

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY at minimum

# 3. Create database
psql -U postgres -c "CREATE DATABASE nihongo;"

# 4. Run migrations
alembic upgrade head

# 5. Seed reference data (kana, vocabulary, kanji)
python seed.py

# 6. Start dev server
uvicorn app.main:app --reload
```

API docs available at: http://localhost:8000/docs

### Running Tests

```bash
# Create test database
psql -U postgres -c "CREATE DATABASE nihongo_test;"

# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

## Deploying to Render

1. Push this repo to GitHub.
2. In Render Dashboard → **New** → **Blueprint** → connect your repo.
3. Render reads `render.yaml` and creates the web service + PostgreSQL database automatically.
4. In the web service's **Environment** tab, set:
   - `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
   - `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`
5. After first deploy completes, run the seed script via Render Shell:
   ```bash
   python seed.py
   ```

### OAuth Callback URLs to register

Add these in Google Cloud Console and GitHub OAuth App settings:

- **Google:** `https://<your-render-service>.onrender.com/auth/google/callback`
- **GitHub:** `https://<your-render-service>.onrender.com/auth/github/callback`

## Environment Variables

See `.env.example` for the full list.
