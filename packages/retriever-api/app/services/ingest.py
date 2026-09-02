from datetime import datetime, timezone
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document # pyright: ignore[reportMissingImports]
from langchain_text_splitters import RecursiveCharacterTextSplitter # pyright: ignore[reportMissingImports]

from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.dependencies import get_vectorstore
from app.services.materials import record_material
from app.services.pdf import delete_temp_pdf


class TextValidationError(ValueError):
    pass


def _ingest_documents(documents: list[Document], *, source: str, doc_type: str) -> int:
    ingested_at = datetime.now(timezone.utc).isoformat()
    for doc in documents:
        doc.metadata.update(
            source=source, type=doc_type, title=source, ingested_at=ingested_at
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    if chunks:
        get_vectorstore().add_documents(chunks)
    return len(chunks)


def ingest_pdf(file_path: Path, filename: str) -> dict:
    try:
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        count = _ingest_documents(documents, source=filename, doc_type="pdf")

        message = (
            "PDF indexado com sucesso."
            if count
            else "PDF processado, mas nenhum texto foi extraído."
        )
        record_material(source=filename, type="pdf", title=filename, chunk_count=count)
        return {"message": message, "filename": filename, "chunks_indexed": count}
    finally:
        delete_temp_pdf(file_path)


def ingest_text(title: str, text: str) -> dict:
    clean_title = title.strip()
    clean_text = text.strip()
    if not clean_title:
        raise TextValidationError("O título não pode ficar vazio.")
    if not clean_text:
        raise TextValidationError("O texto não pode ficar vazio.")

    document = Document(page_content=clean_text)
    count = _ingest_documents([document], source=clean_title, doc_type="text")

    record_material(source=clean_title, type="text", title=clean_title, chunk_count=count)
    return {
        "message": "Texto indexado com sucesso.",
        "source": clean_title,
        "type": "text",
        "chunks_indexed": count,
    }


def list_documents() -> list[dict]:
    result = get_vectorstore().get(include=["metadatas"])
    grouped: dict[str, dict] = {}

    for meta in result.get("metadatas", []):
        source = meta.get("source", "desconhecido")
        entry = grouped.setdefault(
            source,
            {
                "source": source,
                "type": meta.get("type", "pdf"),
                "chunks": 0,
                "ingested_at": meta.get("ingested_at"),
            },
        )
        entry["chunks"] += 1

    return sorted(grouped.values(), key=lambda d: d["source"])
