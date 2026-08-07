import operator
from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langgraph.graph import END, StateGraph

from app.agents.evaluator import evaluate as run_evaluator
from app.agents.planner import plan as run_planner
from app.config import EVALUATOR_MIN_SCORE, MAX_RETRIEVAL_LOOPS, RETRIEVER_K
from app.dependencies import get_llm
from app.prompts.tutor import tutor_prompt
from app.tools.vector_search import search_documents


class RagState(TypedDict):
    question: str
    original_question: str
    history: list[dict]
    needs_retrieval: bool
    context: list[Document]
    score: float
    loops: int
    steps: Annotated[list[dict], operator.add]
    answer: str


def plan_node(state: RagState) -> dict:
    decision = run_planner(state["original_question"], state.get("history", []))
    detail = (
        f"Requer retrieval. Query reescrita: {decision.rewritten_question}"
        if decision.needs_retrieval
        else "Nao requer retrieval. Segue direto para geracao."
    )
    return {
        "question": decision.rewritten_question,
        "needs_retrieval": decision.needs_retrieval,
        "loops": 0,
        "steps": [{"step": "plan", "loop": 0, "detail": detail}],
    }


def retrieve_node(state: RagState) -> dict:
    loop = state["loops"]
    k = RETRIEVER_K * (loop + 1)
    docs = search_documents(state["question"], k=k)
    return {
        "context": docs,
        "steps": [
            {"step": "retrieve", "loop": loop, "detail": f"vector_search retornou {len(docs)} chunks (k={k})"}
        ],
    }


def evaluate_node(state: RagState) -> dict:
    loop = state["loops"]
    result = run_evaluator(state["question"], state["context"])
    return {
        "score": result.score,
        "loops": loop + 1,
        "steps": [{"step": "evaluate", "loop": loop, "detail": f"Score {result.score:.2f}. {result.reasoning}"}],
    }


def augment_node(state: RagState) -> dict:
    loop = max(state["loops"] - 1, 0)
    return {
        "steps": [
            {"step": "augment", "loop": loop, "detail": f"Contexto montado com {len(state['context'])} chunks"}
        ]
    }


def generate_node(state: RagState) -> dict:
    loop = max(state["loops"] - 1, 0)
    context = state.get("context") or []
    if context:
        context_text = "\n\n".join(f"[{d.metadata.get('source')}] {d.page_content}" for d in context)
    else:
        context_text = "Nenhum contexto foi recuperado; esta pergunta nao depende dos documentos do usuario."
    messages = tutor_prompt.format_messages(context=context_text, input=state["original_question"])
    response = get_llm().invoke(messages)
    return {
        "answer": response.content,
        "steps": [{"step": "generate", "loop": loop, "detail": "Resposta gerada"}],
    }


def after_plan(state: RagState) -> str:
    return "retrieve" if state["needs_retrieval"] else "generate"


def after_evaluate(state: RagState) -> str:
    if state["score"] >= EVALUATOR_MIN_SCORE:
        return "augment"
    if state["loops"] >= MAX_RETRIEVAL_LOOPS:
        return "augment"  # fallback: segue com o melhor contexto obtido
    return "retrieve"


def build_graph() -> StateGraph:
    graph = StateGraph(RagState)
    graph.add_node("plan", plan_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("augment", augment_node)
    graph.add_node("generate", generate_node)

    graph.set_entry_point("plan")
    graph.add_conditional_edges("plan", after_plan, {"retrieve": "retrieve", "generate": "generate"})
    graph.add_edge("retrieve", "evaluate")
    graph.add_conditional_edges("evaluate", after_evaluate, {"augment": "augment", "retrieve": "retrieve"})
    graph.add_edge("augment", "generate")
    graph.add_edge("generate", END)
    return graph
