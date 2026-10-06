import httpx

from app.config import EMBED_MODEL, OLLAMA_BASE_URL


def _has_model(names: list[str]) -> bool:
    # O Ollama lista os modelos com tag (ex.: "nomic-embed-text:latest").
    wanted = EMBED_MODEL.split(":")[0]
    return any(name.split(":")[0] == wanted for name in names)


def get_embeddings_status() -> dict:
    """Estado do Ollama usado pelos embeddings (`OLLAMA_BASE_URL`, nao a base URL do LLM)."""
    base = {"model": EMBED_MODEL, "base_url": OLLAMA_BASE_URL}
    try:
        response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        names = [m.get("name", "") for m in response.json().get("models", [])]
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
        return {"status": "unreachable", **base}

    return {"status": "ready" if _has_model(names) else "model_missing", **base}
