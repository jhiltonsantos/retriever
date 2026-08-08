from app.providers.base import LlmProvider
from app.providers.custom import CustomProvider
from app.providers.ollama import OllamaProvider
from app.providers.openrouter import OpenRouterProvider
from app.settings_store import get_effective_config

_PROVIDERS: dict[str, LlmProvider] = {
    "ollama": OllamaProvider(),
    "openrouter": OpenRouterProvider(),
    "custom": CustomProvider(),
}


def get_provider(name: str) -> LlmProvider:
    try:
        return _PROVIDERS[name]
    except KeyError:
        raise ValueError(
            f"LLM_PROVIDER invalido: {name!r}. Use um destes: {', '.join(_PROVIDERS)}."
        ) from None


def get_current_provider() -> LlmProvider:
    return get_provider(get_effective_config().provider)


def normalize_error(exc: Exception) -> Exception:
    return get_current_provider().normalize_error(exc)
