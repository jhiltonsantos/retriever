from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGIN_REGEX, CORS_ORIGINS
from app.db import init_db
from app.routers import ask, conversations, health, ingest, materials, profile, settings, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Retriever API",
        description="Assistente de estudos local com RAG para Programação e Inglês",
        version="0.2.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_origin_regex=CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(upload.router)
    app.include_router(ask.router)
    app.include_router(settings.router)
    app.include_router(ingest.router)
    app.include_router(conversations.router)
    app.include_router(materials.router)
    app.include_router(profile.router)

    return app
