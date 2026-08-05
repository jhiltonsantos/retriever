import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

CHROMA_DIR = Path(os.getenv("CHROMA_DIR", BASE_DIR / "chroma_data"))
TMP_UPLOAD_DIR = Path(os.getenv("TMP_UPLOAD_DIR", BASE_DIR / "tmp_uploads"))

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 4

API_PORT = int(os.getenv("API_PORT", "8000"))
IS_DESKTOP = os.getenv("DESKTOP_MODE", "0") == "1"

CORS_ORIGINS = (
    ["*"]
    if IS_DESKTOP
    else [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]
)
