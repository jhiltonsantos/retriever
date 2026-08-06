import httpx
from langchain_ollama import ChatOllama

from app.providers.base import ModelInfo, TestResult

DEFAULT_MODEL = "llama3"


class OllamaProvider:
    def build_llm(
        self, *, model: str | None, base_url: str, api_key: str | None = None
    ) -> ChatOllama:
        return ChatOllama(model=model or DEFAULT_MODEL, base_url=base_url)

    def list_models(
        self, *, base_url: str, api_key: str | None = None
    ) -> list[ModelInfo]:
        try:
            response = httpx.get(f"{base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise ConnectionError("Nao foi possivel conectar ao Ollama.") from exc

        models = response.json().get("models", [])
        return [
            {"id": m["name"], "label": m["name"]}
            for m in models
            if "embedding" not in m.get("capabilities", [])
        ]

    def test_connection(
        self, *, model: str | None, base_url: str, api_key: str | None = None
    ) -> TestResult:
        try:
            response = httpx.get(f"{base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except httpx.RequestError:
            return {
                "ok": False,
                "reason": "network",
                "message": "Nao foi possivel conectar ao Ollama.",
            }

        names = [m["name"] for m in response.json().get("models", [])]
        if model and model not in names and f"{model}:latest" not in names:
            return {
                "ok": False,
                "reason": "model_not_found",
                "message": f"Modelo '{model}' nao esta instalado no Ollama.",
            }

        return {"ok": True, "reason": None, "message": "Conexao com o Ollama ok."}

    def normalize_error(self, exc: Exception) -> Exception:
        return exc
