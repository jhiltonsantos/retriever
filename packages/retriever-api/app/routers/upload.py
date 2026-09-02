from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ingest import ingest_pdf
from app.services.pdf import PdfValidationError, save_temp_pdf, validate_pdf

router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        validate_pdf(file.content_type, file.filename)
    except PdfValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    filename = file.filename or "documento.pdf"
    content = await file.read()
    temp_path = save_temp_pdf(content, filename)

    try:
        return ingest_pdf(temp_path, filename)
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
