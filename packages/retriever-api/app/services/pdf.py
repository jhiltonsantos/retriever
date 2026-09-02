import uuid
from pathlib import Path

from app.config import TMP_UPLOAD_DIR


class PdfValidationError(ValueError):
    pass


def validate_pdf(content_type: str | None, filename: str | None) -> None:
    if content_type != "application/pdf":
        raise PdfValidationError("Apenas arquivos PDF são aceitos.")

    name = filename or ""
    if not name.lower().endswith(".pdf"):
        raise PdfValidationError("A extensão do arquivo deve ser .pdf")


def save_temp_pdf(content: bytes, filename: str) -> Path:
    TMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(filename).name
    temp_path = TMP_UPLOAD_DIR / f"{uuid.uuid4().hex}_{safe_name}"
    temp_path.write_bytes(content)
    return temp_path


def delete_temp_pdf(file_path: Path) -> None:
    if file_path.exists():
        file_path.unlink()
