from app.dependencies import reset_llm_cache
from app.providers.registry import get_provider
from app.settings_store import (
    EffectiveLlmConfig,
    default_base_url,
    get_effective_config,
    mask_key,
    write_settings,
)

KNOWN_PROVIDERS = {"ollama", "openrouter"}


def _validate_provider(provider: str) -> None:
    if provider not in KNOWN_PROVIDERS:
        raise ValueError(
            f"Provedor invalido: {provider!r}. Use um destes: {', '.join(KNOWN_PROVIDERS)}."
        )


def _to_response(cfg: EffectiveLlmConfig) -> dict:
    return {
        "provider": cfg.provider,
        "model": cfg.model,
        "base_url": cfg.base_url,
        "api_key_masked": mask_key(cfg.api_key),
        "api_key_set": bool(cfg.api_key),
    }


def get_llm_settings() -> dict:
    return _to_response(get_effective_config())


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
    return _to_response(get_effective_config())


def list_llm_models(provider: str | None = None) -> dict:
    cfg = get_effective_config()
    target = provider or cfg.provider
    _validate_provider(target)
    base_url = cfg.base_url if target == cfg.provider else default_base_url(target)
    models = get_provider(target).list_models(base_url=base_url, api_key=cfg.api_key)
    return {"provider": target, "models": models}


def test_llm_connection(payload) -> dict:
    _validate_provider(payload.provider)
    provider = get_provider(payload.provider)
    base_url = payload.base_url or default_base_url(payload.provider)
    # Chave em branco testa com a que ja esta salva/no .env, nao falha de cara -
    # a UI nunca recebe a chave em claro de volta pra reenviar.
    api_key = payload.api_key or get_effective_config().api_key
    return provider.test_connection(
        model=payload.model, base_url=base_url, api_key=api_key
    )
