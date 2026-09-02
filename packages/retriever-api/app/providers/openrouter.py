from app.providers._openai_compatible import (
    build_openai_compatible_llm,
    classify_openai_error,
    list_openai_compatible_models,
    test_openai_compatible_connection,
)
from app.providers.base import ProviderRequestError

DEFAULT_MODEL = "deepseek/deepseek-v4-flash-0731"  # barato e com tool calling confiavel, ver docs/providers.md

HEADERS = {
    "HTTP-Referer": "https://github.com/jhiltonsantos/retriever",
    "X-Title": "Retriever",
}

LABEL = "OpenRouter"


class OpenRouterProvider:
    def build_llm(self, *, model, base_url, api_key):
        return build_openai_compatible_llm(
            model=model,
            base_url=base_url,
            api_key=api_key,
            default_model=DEFAULT_MODEL,
            require_api_key=True,
            extra_headers=HEADERS,
            provider_label=LABEL,
        )

    def list_models(self, *, base_url, api_key):
        return list_openai_compatible_models(base_url=base_url, api_key=api_key, provider_label=LABEL)

    def test_connection(self, *, model, base_url, api_key):
        return test_openai_compatible_connection(
            model=model,
            base_url=base_url,
            api_key=api_key,
            default_model=DEFAULT_MODEL,
            require_api_key=True,
            extra_headers=HEADERS,
            provider_label=LABEL,
        )

    def normalize_error(self, exc: Exception) -> Exception:
        classified = classify_openai_error(exc, LABEL)
        if classified is None:
            return exc
        _, message = classified
        return ProviderRequestError(message)
