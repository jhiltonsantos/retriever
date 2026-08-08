import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
LLM_MODEL = os.getenv("LLM_MODEL") or None
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://openrouter.ai/api/v1")

CHROMA_DIR = Path(os.getenv("CHROMA_DIR", BASE_DIR / "chroma_data"))
TMP_UPLOAD_DIR = Path(os.getenv("TMP_UPLOAD_DIR", BASE_DIR / "tmp_uploads"))
SETTINGS_DIR = Path(os.getenv("SETTINGS_DIR", BASE_DIR / "user_data"))

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 4

MAX_RETRIEVAL_LOOPS = int(os.getenv("MAX_RETRIEVAL_LOOPS", "2"))
EVALUATOR_MIN_SCORE = float(os.getenv("EVALUATOR_MIN_SCORE", "0.6"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))

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
