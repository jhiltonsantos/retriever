from dataclasses import dataclass
from datetime import datetime, timezone

from app.config import LLM_API_KEY, LLM_PROVIDER, OLLAMA_BASE_URL
from app.db import get_connection

OPENROUTER_DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
_ALL_PROVIDERS = ("ollama", "openrouter", "custom")


def default_base_url(provider: str) -> str:
    if provider == "ollama":
        return OLLAMA_BASE_URL
    if provider == "openrouter":
        return OPENROUTER_DEFAULT_BASE_URL
    return ""  # "custom" nao tem default sensato


@dataclass
class EffectiveLlmConfig:
    provider: str
    model: str | None
    base_url: str
    api_key: str | None


def _read_row(provider: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT model, base_url, api_key FROM llm_provider_settings WHERE provider = ?",
            (provider,),
        ).fetchone()
    return dict(row) if row else None


def get_active_provider() -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = 'active_llm_provider'"
        ).fetchone()
    return row["value"] if row else LLM_PROVIDER


def set_active_provider(provider: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO app_settings (key, value) VALUES ('active_llm_provider', ?)
               ON CONFLICT(key) DO UPDATE SET value = excluded.value""",
            (provider,),
        )


def get_provider_settings(provider: str) -> EffectiveLlmConfig:
    row = _read_row(provider)
    saved = row or {}

    api_key = saved.get("api_key")
    if not api_key and row is None and provider == LLM_PROVIDER:
        # Fallback de config zero: LLM_API_KEY so preenche o provedor default do
        # .env, e so enquanto ele nunca foi salvo no banco (preserva deploys
        # via env var, ex.: injecao futura de chave no desktop).
        api_key = LLM_API_KEY or None

    return EffectiveLlmConfig(
        provider=provider,
        model=saved.get("model"),
        base_url=saved.get("base_url") or default_base_url(provider),
        api_key=api_key,
    )


def get_effective_config() -> EffectiveLlmConfig:
    return get_provider_settings(get_active_provider())


def write_settings(payload: dict) -> None:
    provider = payload["provider"]
    current = _read_row(provider) or {}
    merged = {
        "model": payload.get("model") if payload.get("model") is not None else current.get("model"),
        "base_url": payload.get("base_url") if payload.get("base_url") is not None else current.get("base_url"),
        "api_key": payload.get("api_key") if payload.get("api_key") is not None else current.get("api_key"),
    }
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO llm_provider_settings (provider, model, base_url, api_key, updated_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(provider) DO UPDATE SET
                 model=excluded.model, base_url=excluded.base_url,
                 api_key=excluded.api_key, updated_at=excluded.updated_at""",
            (provider, merged["model"], merged["base_url"], merged["api_key"], now),
        )
    set_active_provider(provider)


def list_all_provider_settings() -> dict[str, EffectiveLlmConfig]:
    return {p: get_provider_settings(p) for p in _ALL_PROVIDERS}


def mask_key(key: str | None) -> str | None:
    if not key:
        return None
    if len(key) <= 10:
        return "..." + key[-2:]
    return f"{key[:6]}...{key[-4:]}"
