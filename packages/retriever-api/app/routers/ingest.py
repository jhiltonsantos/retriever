from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ingest import TextValidationError, ingest_text, list_documents

router = APIRouter(tags=["ingest"])


class IngestTextPayload(BaseModel):
    title: str
    text: str


@router.post("/ingest/text")
async def ingest_text_endpoint(payload: IngestTextPayload):
    try:
        return ingest_text(payload.title, payload.text)
    except TextValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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


@router.get("/documents")
async def get_documents():
    return {"documents": list_documents()}
