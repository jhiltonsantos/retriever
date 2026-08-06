from app.dependencies import get_retrieval_chain
from app.providers.registry import normalize_error


def ask_question(question: str) -> str:
    chain = get_retrieval_chain()
    try:
        result = chain.invoke({"input": question})
    except Exception as exc:
        raise normalize_error(exc) from exc
    return result["answer"]
