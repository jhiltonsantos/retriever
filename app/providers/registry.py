from app.config import LLM_PROVIDER
from app.providers.base import LlmProvider
from app.providers.ollama import OllamaProvider
from app.providers.openrouter import OpenRouterProvider

_PROVIDERS: dict[str, LlmProvider] = {
    "ollama": OllamaProvider(),
    "openrouter": OpenRouterProvider(),
}


def get_provider() -> LlmProvider:
    try:
        return _PROVIDERS[LLM_PROVIDER]
    except KeyError:
        raise ValueError(
            f"LLM_PROVIDER invalido: {LLM_PROVIDER!r}. "
            f"Use um destes: {', '.join(_PROVIDERS)}."
        ) from None


def normalize_error(exc: Exception) -> Exception:
    return get_provider().normalize_error(exc)
