from app.config import EMBED_MODEL, EMBED_PROVIDER, OLLAMA_BASE_URL
from app.providers.embeddings.registry import get_embeddings_provider


def get_embeddings_status() -> dict:
    """Estado do provedor de embeddings (hoje so Ollama, em `OLLAMA_BASE_URL`, nao a base URL do LLM)."""
    provider = get_embeddings_provider(EMBED_PROVIDER)
    result = provider.check_status(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)
    return {**result, "provider": EMBED_PROVIDER, "model": EMBED_MODEL, "base_url": OLLAMA_BASE_URL}
