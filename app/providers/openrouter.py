import httpx
from langchain_openai import ChatOpenAI

from app.providers.base import (
    ModelInfo,
    ProviderConfigError,
    ProviderRequestError,
    TestResult,
)

DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct"

HEADERS = {
    "HTTP-Referer": "https://github.com/jhiltonsantos/retriever",
    "X-Title": "Retriever",
}


def _classify(exc: Exception) -> tuple[str, str] | None:
    from openai import (
        APIConnectionError,
        APITimeoutError,
        AuthenticationError,
        BadRequestError,
        NotFoundError,
        RateLimitError,
    )

    if isinstance(exc, AuthenticationError):
        return "auth", "Falha de autenticacao com o provedor remoto (OpenRouter)."
    if isinstance(exc, RateLimitError):
        return "quota", "Cota excedida no provedor remoto (OpenRouter)."
    if isinstance(exc, (NotFoundError, BadRequestError)):
        return (
            "model_not_found",
            "Modelo invalido ou nao encontrado no OpenRouter.",
        )
    if isinstance(exc, (APITimeoutError, APIConnectionError)):
        return "network", "Nao foi possivel contatar o provedor remoto (OpenRouter)."
    return None


class OpenRouterProvider:
    def build_llm(
        self, *, model: str | None, base_url: str, api_key: str | None
    ) -> ChatOpenAI:
        if not api_key:
            raise ProviderConfigError(
                "Nenhuma chave de API configurada para o provedor remoto. "
                "Configure LLM_API_KEY para usar o OpenRouter."
            )
        return ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model or DEFAULT_MODEL,
            default_headers=HEADERS,
        )

    def list_models(
        self, *, base_url: str, api_key: str | None
    ) -> list[ModelInfo]:
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        try:
            response = httpx.get(f"{base_url}/models", headers=headers, timeout=10)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise ProviderRequestError(
                "Nao foi possivel contatar o provedor remoto (OpenRouter)."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderRequestError(
                "O provedor remoto (OpenRouter) rejeitou a listagem de modelos."
            ) from exc

        data = response.json().get("data", [])
        return [{"id": m["id"], "label": m.get("name", m["id"])} for m in data]

    def test_connection(
        self, *, model: str | None, base_url: str, api_key: str | None
    ) -> TestResult:
        if not api_key:
            return {
                "ok": False,
                "reason": "auth",
                "message": "Nenhuma chave de API informada.",
            }
        try:
            llm = ChatOpenAI(
                base_url=base_url,
                api_key=api_key,
                model=model or DEFAULT_MODEL,
                default_headers=HEADERS,
                max_tokens=16,
            )
            llm.invoke("ping")
        except Exception as exc:
            classified = _classify(exc)
            if classified is None:
                return {"ok": False, "reason": "network", "message": str(exc)}
            reason, message = classified
            return {"ok": False, "reason": reason, "message": message}

        return {"ok": True, "reason": None, "message": "Conexao com o OpenRouter ok."}

    def normalize_error(self, exc: Exception) -> Exception:
        classified = _classify(exc)
        if classified is None:
            return exc
        _, message = classified
        return ProviderRequestError(message)
