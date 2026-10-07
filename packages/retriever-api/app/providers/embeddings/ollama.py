import httpx
from langchain_ollama import OllamaEmbeddings

from app.providers.embeddings.base import EmbeddingsStatus


def _has_model(names: list[str], model: str) -> bool:
    # O Ollama lista os modelos com tag (ex.: "nomic-embed-text:latest").
    wanted = model.split(":")[0]
    return any(name.split(":")[0] == wanted for name in names)


class OllamaEmbeddingsProvider:
    def build(self, *, model: str, base_url: str) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=model, base_url=base_url)

    def check_status(self, *, model: str, base_url: str) -> EmbeddingsStatus:
        try:
            response = httpx.get(f"{base_url}/api/tags", timeout=5)
            response.raise_for_status()
            names = [m.get("name", "") for m in response.json().get("models", [])]
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
            return {"status": "unreachable"}

        return {"status": "ready" if _has_model(names, model) else "model_missing"}
