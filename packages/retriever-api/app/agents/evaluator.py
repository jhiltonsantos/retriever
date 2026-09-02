from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.dependencies import get_llm
from app.prompts.evaluator import EVALUATOR_SYSTEM_PROMPT


class EvaluationResult(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Nota de 0 a 1 para a relevancia do contexto.")
    reasoning: str = Field(description="Justificativa curta da nota, em uma frase.")


def evaluate(question: str, context: list[Document]) -> EvaluationResult:
    if not context:
        return EvaluationResult(score=0.0, reasoning="Nenhum trecho recuperado.")

    llm = get_llm().with_structured_output(EvaluationResult)
    context_text = "\n\n".join(f"[{d.metadata.get('source')}] {d.page_content}" for d in context)
    messages = [
        SystemMessage(EVALUATOR_SYSTEM_PROMPT),
        HumanMessage(f"Pergunta: {question}\n\nContexto recuperado:\n{context_text}"),
    ]
    return llm.invoke(messages)
