import json
import os
from dataclasses import dataclass

from app.config import (
    LLM_API_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    SETTINGS_DIR,
)

SETTINGS_FILE = SETTINGS_DIR / "settings.json"


def default_base_url(provider: str) -> str:
    return OLLAMA_BASE_URL if provider == "ollama" else LLM_API_BASE_URL


@dataclass
class EffectiveLlmConfig:
    provider: str
    model: str | None
    base_url: str
    api_key: str | None


def read_settings() -> dict | None:
    if not SETTINGS_FILE.exists():
        return None
    return json.loads(SETTINGS_FILE.read_text())


def write_settings(partial: dict) -> None:
    current = read_settings() or {}
    current.update({k: v for k, v in partial.items() if v is not None})
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(current, indent=2))
    os.chmod(SETTINGS_FILE, 0o600)


def get_effective_config() -> EffectiveLlmConfig:
    saved = read_settings() or {}
    provider = saved.get("provider") or LLM_PROVIDER
    return EffectiveLlmConfig(
        provider=provider,
        model=saved.get("model") or LLM_MODEL,
        base_url=saved.get("base_url") or default_base_url(provider),
        api_key=saved.get("api_key") or LLM_API_KEY or None,
    )


def mask_key(key: str | None) -> str | None:
    if not key:
        return None
    if len(key) <= 10:
        return "..." + key[-2:]
    return f"{key[:6]}...{key[-4:]}"
