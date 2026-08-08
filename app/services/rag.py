from app.dependencies import get_agent_graph
from app.providers.registry import normalize_error
from app.services.conversations import add_message
from app.services.memory import normalize_history
from app.tools.vector_search import documents_to_sources


def ask_question(
    question: str,
    history: list[dict] | None = None,
    conversation_id: str | None = None,
) -> dict:
    graph = get_agent_graph()
    initial_state = {
        "question": question,
        "original_question": question,
        "history": normalize_history(history),
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

    sources = documents_to_sources(final_state.get("context") or [])
    agent_steps = final_state["steps"]
    answer = final_state["answer"]

    if conversation_id:
        add_message(
            conversation_id=conversation_id,
            role="user",
            content=question,
        )
        add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            sources=sources,
            agent_steps=agent_steps,
        )

    return {
        "answer": answer,
        "sources": sources,
        "agent_steps": agent_steps,
    }
