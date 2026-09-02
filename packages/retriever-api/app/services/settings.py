from app.dependencies import reset_llm_cache
from app.providers.registry import get_provider
from app.settings_store import (
    EffectiveLlmConfig,
    default_base_url,
    get_active_provider,
    get_provider_settings,
    list_all_provider_settings,
    mask_key,
    write_settings,
)

KNOWN_PROVIDERS = {"ollama", "openrouter", "custom"}


def _validate_provider(provider: str) -> None:
    if provider not in KNOWN_PROVIDERS:
        raise ValueError(
            f"Provedor invalido: {provider!r}. Use um destes: {', '.join(KNOWN_PROVIDERS)}."
        )


def _provider_to_dict(cfg: EffectiveLlmConfig) -> dict:
    return {
        "model": cfg.model,
        "base_url": cfg.base_url,
        "api_key_masked": mask_key(cfg.api_key),
        "api_key_set": bool(cfg.api_key),
    }


def _full_snapshot() -> dict:
    return {
        "active_provider": get_active_provider(),
        "providers": {p: _provider_to_dict(cfg) for p, cfg in list_all_provider_settings().items()},
    }


def get_llm_settings() -> dict:
    return _full_snapshot()


def update_llm_settings(payload) -> dict:
    _validate_provider(payload.provider)

    write_settings(
        {
            "provider": payload.provider,
            "model": payload.model,
            "base_url": payload.base_url or default_base_url(payload.provider),
            "api_key": payload.api_key,
        }
    )
    reset_llm_cache()
    return _full_snapshot()


def list_llm_models(provider: str | None = None) -> dict:
    target = provider or get_active_provider()
    _validate_provider(target)
    # Usa a config salva do proprio provedor pre-visualizado, nao a do provedor
    # ativo - previamente isso reusava a api_key/base_url do provedor ativo
    # mesmo pre-visualizando um provedor diferente via ?provider=.
    cfg = get_provider_settings(target)
    models = get_provider(target).list_models(base_url=cfg.base_url, api_key=cfg.api_key)
    return {"provider": target, "models": models}


def test_llm_connection(payload) -> dict:
    _validate_provider(payload.provider)
    provider = get_provider(payload.provider)
    base_url = payload.base_url or default_base_url(payload.provider)
    # Chave em branco testa com a que ja esta salva para ESSE provedor (nao o
    # ativo) - a UI nunca recebe a chave em claro de volta pra reenviar.
    api_key = payload.api_key or get_provider_settings(payload.provider).api_key
    return provider.test_connection(
        model=payload.model, base_url=base_url, api_key=api_key
    )
