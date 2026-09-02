from langchain_core.tools import tool


@tool
def list_documents() -> str:
    """Lista os documentos (PDF e texto) que o usuario ja indexou, com a quantidade de trechos de cada um."""
    from app.services.ingest import list_documents as get_indexed_documents

    docs = get_indexed_documents()
    if not docs:
        return "Nenhum documento indexado ainda."
    return "\n".join(f"- {d['source']} ({d['type']}, {d['chunks']} trechos)" for d in docs)
