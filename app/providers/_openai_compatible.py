import httpx
from langchain_openai import ChatOpenAI

from app.providers.base import ModelInfo, ProviderConfigError, ProviderRequestError, TestResult


def classify_openai_error(exc: Exception, provider_label: str) -> tuple[str, str] | None:
    from openai import (
        APIConnectionError,
        APITimeoutError,
        AuthenticationError,
        BadRequestError,
        NotFoundError,
        RateLimitError,
    )

    if isinstance(exc, AuthenticationError):
        return "auth", f"Falha de autenticacao com o provedor remoto ({provider_label})."
    if isinstance(exc, RateLimitError):
        return "quota", f"Cota excedida no provedor remoto ({provider_label})."
    if isinstance(exc, (NotFoundError, BadRequestError)):
        return "model_not_found", f"Modelo invalido ou nao encontrado no {provider_label}."
    if isinstance(exc, (APITimeoutError, APIConnectionError)):
        return "network", f"Nao foi possivel contatar o provedor remoto ({provider_label})."
    return None


def build_openai_compatible_llm(
    *,
    model: str | None,
    base_url: str,
    api_key: str | None,
    default_model: str | None,
    require_api_key: bool,
    extra_headers: dict | None,
    provider_label: str,
) -> ChatOpenAI:
    if require_api_key and not api_key:
        raise ProviderConfigError(
            f"Nenhuma chave de API configurada para o provedor remoto ({provider_label})."
        )
    if not base_url:
        raise ProviderConfigError(f"Base URL obrigatoria para o provedor {provider_label}.")
    resolved_model = model or default_model
    if not resolved_model:
        raise ProviderConfigError(f"Modelo obrigatorio para o provedor {provider_label}.")

    kwargs = {"base_url": base_url, "api_key": api_key or "not-required", "model": resolved_model}
    if extra_headers:
        kwargs["default_headers"] = extra_headers
    return ChatOpenAI(**kwargs)


def list_openai_compatible_models(*, base_url: str, api_key: str | None, provider_label: str) -> list[ModelInfo]:
    if not base_url:
        raise ProviderConfigError(f"Base URL obrigatoria para o provedor {provider_label}.")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    try:
        response = httpx.get(f"{base_url}/models", headers=headers, timeout=10)
        response.raise_for_status()
    except httpx.RequestError as exc:
        raise ProviderRequestError(
            f"Nao foi possivel contatar o provedor remoto ({provider_label})."
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise ProviderRequestError(
            f"O provedor remoto ({provider_label}) rejeitou a listagem de modelos."
        ) from exc

    data = response.json().get("data", [])
    return [{"id": m["id"], "label": m.get("name", m["id"])} for m in data]


def test_openai_compatible_connection(
    *,
    model: str | None,
    base_url: str,
    api_key: str | None,
    default_model: str | None,
    require_api_key: bool,
    extra_headers: dict | None,
    provider_label: str,
) -> TestResult:
    if require_api_key and not api_key:
        return {"ok": False, "reason": "auth", "message": "Nenhuma chave de API informada."}
    if not base_url:
        return {
            "ok": False,
            "reason": "network",
            "message": f"Base URL obrigatoria para o provedor {provider_label}.",
        }
    resolved_model = model or default_model
    if not resolved_model:
        return {
            "ok": False,
            "reason": "model_not_found",
            "message": f"Modelo obrigatorio para o provedor {provider_label}.",
        }

    try:
        kwargs = {
            "base_url": base_url,
            "api_key": api_key or "not-required",
            "model": resolved_model,
            "max_tokens": 16,
        }
        if extra_headers:
            kwargs["default_headers"] = extra_headers
        ChatOpenAI(**kwargs).invoke("ping")
    except Exception as exc:
        classified = classify_openai_error(exc, provider_label)
        if classified is None:
            return {"ok": False, "reason": "network", "message": str(exc)}
        reason, message = classified
        return {"ok": False, "reason": reason, "message": message}

    return {"ok": True, "reason": None, "message": f"Conexao com o {provider_label} ok."}
