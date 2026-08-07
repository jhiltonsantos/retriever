from langchain_core.documents import Document
from langchain_core.tools import tool


def search_documents(query: str, k: int | None = None) -> list[Document]:
    """Busca por similaridade no vectorstore e devolve os Documents crus."""
    from app.config import RETRIEVER_K
    from app.dependencies import get_vectorstore

    return get_vectorstore().similarity_search(query, k=k or RETRIEVER_K)


def documents_to_sources(docs: list[Document]) -> list[dict]:
    return [
        {
            "source": d.metadata.get("source"),
            "type": d.metadata.get("type", "pdf"),
            "page": d.metadata.get("page"),
            "snippet": d.page_content[:200],
        }
        for d in docs
    ]


@tool(response_format="content_and_artifact")
def vector_search(query: str) -> tuple[str, list[dict]]:
    """Busca trechos relevantes nos documentos que o usuario ja indexou (PDF ou texto) para responder a pergunta dele."""
    docs = search_documents(query)
    if not docs:
        return "Nenhum trecho relevante encontrado nos documentos indexados.", []

    content = "\n\n".join(f"[{d.metadata.get('source')}] {d.page_content}" for d in docs)
    return content, documents_to_sources(docs)
