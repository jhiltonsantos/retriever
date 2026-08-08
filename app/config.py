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
GRAPH_MUTUAL_KNN_K = int(os.getenv("GRAPH_MUTUAL_KNN_K", "3"))

API_PORT = int(os.getenv("API_PORT", "8000"))
IS_DESKTOP = os.getenv("DESKTOP_MODE", "0") == "1"

CORS_ORIGINS = ["*"] if IS_DESKTOP else []
# Vite pula para a proxima porta livre (5174, 5175...) quando 5173 esta ocupada
# -- por regex em vez de lista fixa, para nao quebrar sempre que isso acontecer.
CORS_ORIGIN_REGEX = None if IS_DESKTOP else r"^https?://(localhost|127\.0\.0\.1):\d+$"
