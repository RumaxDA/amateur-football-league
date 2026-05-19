from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.routes import (
    user,
    player,
    team,
    match,
    tournament,
    action,
    tournament_table,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()

docs_url = "/docs" if settings.ENVIRONMENT == "dev" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "dev" else None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tworzenie tabel przy starcie aplikacji
    Base.metadata.create_all(bind=engine)
    yield
    # Zamknięcie połączeń z bazą danych przy wyłączaniu aplikacji
    engine.dispose()


app = FastAPI(
    title="AFL System",
    lifespan=lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

origins = [settings.FRONTEND_URL]

if settings.ENVIRONMENT == "dev":
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user.router)
app.include_router(player.router)
app.include_router(team.router)
app.include_router(match.router)
app.include_router(action.router)
app.include_router(tournament.router)
app.include_router(tournament_table.router)


@app.get("/")
def health_check():
    return {"status": "online"}