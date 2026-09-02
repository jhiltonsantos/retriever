from langchain_core.tools import tool


@tool
def summarize_chunks(source: str) -> str:
    """Busca todos os trechos indexados de um documento especifico, pelo nome exato retornado por list_documents, para o modelo resumir. Use quando o usuario pedir um resumo de um documento."""
    from app.dependencies import get_vectorstore

    result = get_vectorstore().get(where={"source": source}, include=["documents"])
    docs = result.get("documents", [])
    if not docs:
        return f"Nenhum trecho encontrado para a fonte '{source}'."
    return "\n\n".join(docs)
