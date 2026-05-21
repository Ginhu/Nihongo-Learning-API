from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.routers import auth, content, settings as settings_router, progress, flashcards, favorites

app = FastAPI(title="Nihongo Master API")

@app.on_event("startup")
async def startup():
    import sys
    print(f"[CORS] Allowed origins: {settings.get_cors_origins()}", file=sys.stderr, flush=True)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(settings_router.router)
app.include_router(progress.router)
app.include_router(flashcards.router)
app.include_router(favorites.router)
