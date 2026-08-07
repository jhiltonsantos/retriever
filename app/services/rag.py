from app.dependencies import get_agent_graph
from app.providers.registry import normalize_error
from app.tools.vector_search import documents_to_sources


def ask_question(question: str) -> dict:
    graph = get_agent_graph()
    initial_state = {
        "question": question,
        "original_question": question,
        "history": [],
        "needs_retrieval": False,
        "context": [],
        "score": 0.0,
        "loops": 0,
        "steps": [],
        "answer": "",
    }
    try:
        final_state = graph.invoke(initial_state)
    except Exception as exc:
        raise normalize_error(exc) from exc

    return {
        "answer": final_state["answer"],
        "sources": documents_to_sources(final_state.get("context") or []),
        "agent_steps": final_state["steps"],
    }
