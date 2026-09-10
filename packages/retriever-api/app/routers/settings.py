from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.providers.base import ProviderConfigError, ProviderRequestError
from app.services import settings as settings_service
from app.settings_store import KeyringUnavailableError

router = APIRouter(prefix="/settings", tags=["settings"])


class LlmSettingsPayload(BaseModel):
    provider: str
    model: str
    base_url: str | None = None
    api_key: str | None = None


@router.get("/llm")
async def get_llm_settings():
    try:
        return settings_service.get_llm_settings()
    except KeyringUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Nao foi possivel acessar o keyring do sistema para ler a chave de API.",
        ) from exc


@router.put("/llm")
async def update_llm_settings(payload: LlmSettingsPayload):
    try:
        return settings_service.update_llm_settings(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyringUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Nao foi possivel acessar o keyring do sistema para gravar a chave de API.",
        ) from exc


@router.get("/llm/models")
async def get_llm_models(provider: str | None = None):
    try:
        return settings_service.list_llm_models(provider)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ProviderConfigError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ProviderRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Modelos indisponíveis. Verifique se o app está rodando na bandeja.",
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar aos modelos em localhost:11434.",
        ) from exc
    except KeyringUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Nao foi possivel acessar o keyring do sistema para ler a chave de API.",
        ) from exc


@router.post("/llm/test")
async def test_llm_connection(payload: LlmSettingsPayload):
    try:
        return settings_service.test_llm_connection(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyringUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Nao foi possivel acessar o keyring do sistema para ler a chave de API.",
        ) from exc
