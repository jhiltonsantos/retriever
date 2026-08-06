from langchain_openai import ChatOpenAI

from app.config import LLM_API_BASE_URL, LLM_API_KEY, LLM_MODEL
from app.providers.base import ProviderRequestError, ProviderConfigError

DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct"

HEADERS = {
    "HTTP-Referer": "https://github.com/jhiltonsantos/retriever",
    "X-Title": "Retriever",
}


class OpenRouterProvider:
    def build_llm(self) -> ChatOpenAI:
        if not LLM_API_KEY:
            raise ProviderConfigError(
                "Nenhuma chave de API configurada para o provedor remoto. "
                "Configure LLM_API_KEY para usar o OpenRouter."
            )
        return ChatOpenAI(
            base_url=LLM_API_BASE_URL,
            api_key=LLM_API_KEY,
            model=LLM_MODEL or DEFAULT_MODEL,
            default_headers=HEADERS,
        )

    def normalize_error(self, exc: Exception) -> Exception:
        from openai import (
            APIConnectionError,
            APITimeoutError,
            AuthenticationError,
            RateLimitError,
        )

        if isinstance(exc, AuthenticationError):
            return ProviderRequestError(
                "Falha de autenticacao com o provedor remoto (OpenRouter)."
            )
        if isinstance(exc, RateLimitError):
            return ProviderRequestError(
                "Cota excedida no provedor remoto (OpenRouter)."
            )
        if isinstance(exc, (APITimeoutError, APIConnectionError)):
            return ProviderRequestError(
                "Nao foi possivel contatar o provedor remoto (OpenRouter)."
            )
        return exc
