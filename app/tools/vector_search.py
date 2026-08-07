from langchain_core.tools import tool


@tool(response_format="content_and_artifact")
def vector_search(query: str) -> tuple[str, list[dict]]:
    """Busca trechos relevantes nos documentos que o usuario ja indexou (PDF ou texto) para responder a pergunta dele."""
    from app.config import RETRIEVER_K
    from app.dependencies import get_vectorstore

    docs = get_vectorstore().similarity_search(query, k=RETRIEVER_K)
    if not docs:
        return "Nenhum trecho relevante encontrado nos documentos indexados.", []

    content = "\n\n".join(f"[{d.metadata.get('source')}] {d.page_content}" for d in docs)
    sources = [
        {
            "source": d.metadata.get("source"),
            "type": d.metadata.get("type", "pdf"),
            "page": d.metadata.get("page"),
            "snippet": d.page_content[:200],
        }
        for d in docs
    ]
    return content, sources
