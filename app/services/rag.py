from langchain_core.messages import HumanMessage, SystemMessage

from app.dependencies import get_agent_llm
from app.prompts.agent import AGENT_SYSTEM_PROMPT
from app.providers.registry import normalize_error
from app.tools import TOOLS

MAX_TOOL_ROUNDS = 3
_TOOLS_BY_NAME = {t.name: t for t in TOOLS}


def ask_question(question: str) -> dict:
    llm = get_agent_llm()
    messages = [SystemMessage(AGENT_SYSTEM_PROMPT), HumanMessage(question)]
    sources: list[dict] = []

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            response = llm.invoke(messages)
            if not response.tool_calls:
                return _build_result(response.content, sources)

            messages.append(response)
            for call in response.tool_calls:
                tool_message = _TOOLS_BY_NAME[call["name"]].invoke(call)
                messages.append(tool_message)
                if tool_message.artifact:
                    sources.extend(tool_message.artifact)

        response = llm.invoke(messages)
        return _build_result(response.content, sources)
    except Exception as exc:
        raise normalize_error(exc) from exc


def _build_result(answer: str, sources: list[dict]) -> dict:
    return {"answer": answer, "sources": sources}
