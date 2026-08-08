from app.providers._openai_compatible import (
    build_openai_compatible_llm,
    classify_openai_error,
    list_openai_compatible_models,
    test_openai_compatible_connection,
)
from app.providers.base import ProviderRequestError

LABEL = "Custom"


class CustomProvider:
    """Qualquer endpoint compativel com a API da OpenAI (LM Studio, vLLM,
    servidor auto-hospedado, etc). Sem modelo default e sem headers especiais;
    a chave de API e opcional pois muitos servidores locais nao exigem auth."""

    def build_llm(self, *, model, base_url, api_key):
        return build_openai_compatible_llm(
            model=model,
            base_url=base_url,
            api_key=api_key,
            default_model=None,
            require_api_key=False,
            extra_headers=None,
            provider_label=LABEL,
        )

    def list_models(self, *, base_url, api_key):
        return list_openai_compatible_models(base_url=base_url, api_key=api_key, provider_label=LABEL)

    def test_connection(self, *, model, base_url, api_key):
        return test_openai_compatible_connection(
            model=model,
            base_url=base_url,
            api_key=api_key,
            default_model=None,
            require_api_key=False,
            extra_headers=None,
            provider_label=LABEL,
        )

    def normalize_error(self, exc: Exception) -> Exception:
        classified = classify_openai_error(exc, LABEL)
        if classified is None:
            return exc
        _, message = classified
        return ProviderRequestError(message)
