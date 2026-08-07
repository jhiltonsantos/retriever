from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.dependencies import get_llm
from app.prompts.planner import PLANNER_SYSTEM_PROMPT


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
    # `history` existe na assinatura para nao quebrar quando F-MEM comecar a
    # popula-lo; em F-AGENT ele chega sempre vazio e nao e usado no prompt.
    llm = get_llm().with_structured_output(PlannerDecision)
    messages = [SystemMessage(PLANNER_SYSTEM_PROMPT), HumanMessage(question)]
    return llm.invoke(messages)
