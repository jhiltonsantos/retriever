from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.routers import ask, health, settings, upload


def create_app() -> FastAPI:
    app = FastAPI(
        title="Retriever API",
        description="Assistente de estudos local com RAG para Programação e Inglês",
        version="0.2.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(upload.router)
    app.include_router(ask.router)
    app.include_router(settings.router)

    return app
