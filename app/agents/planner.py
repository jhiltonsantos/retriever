from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.dependencies import get_llm
from app.prompts.planner import PLANNER_SYSTEM_PROMPT
from app.services.memory import history_to_messages


class PlannerDecision(BaseModel):
    needs_retrieval: bool = Field(
        description="Se a pergunta exige buscar nos documentos indexados pelo usuario."
    )
    rewritten_question: str = Field(
        description=(
            "A pergunta reescrita como query autocontida, otimizada para busca por "
            "similaridade. Se needs_retrieval for falso, repita a pergunta original aqui."
        )
    )


def plan(question: str, history: list[dict]) -> PlannerDecision:
    llm = get_llm().with_structured_output(PlannerDecision)
    messages = [
        SystemMessage(PLANNER_SYSTEM_PROMPT),
        *history_to_messages(history),
        HumanMessage(question),
    ]
    return llm.invoke(messages)
