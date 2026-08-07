from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from app.config import MAX_HISTORY_MESSAGES

_ALLOWED_ROLES = {"user", "assistant"}
_ROLE_TO_MESSAGE = {"user": HumanMessage, "assistant": AIMessage}


def normalize_history(raw_history: list[dict] | None) -> list[dict]:
    """Normaliza o history[] recebido no corpo do /ask.

    Descarta entradas malformadas (role fora de user/assistant, content vazio
    ou nao-string) e mantem so as MAX_HISTORY_MESSAGES mensagens mais
    recentes. Puramente funcional: nada e lido ou escrito fora do parametro
    recebido, a API permanece stateless entre requisicoes.
    """
    if not raw_history:
        return []

    normalized: list[dict] = []
    for item in raw_history:
        role = item.get("role") if isinstance(item, dict) else None
        content = item.get("content") if isinstance(item, dict) else None
        if role not in _ALLOWED_ROLES:
            continue
        if not isinstance(content, str) or not content.strip():
            continue
        normalized.append({"role": role, "content": content.strip()})

    return normalized[-MAX_HISTORY_MESSAGES:]


def history_to_messages(history: list[dict]) -> list[BaseMessage]:
    """Converte history[] (ja normalizado) em HumanMessage/AIMessage, na ordem."""
    messages: list[BaseMessage] = []
    for turn in history:
        message_cls = _ROLE_TO_MESSAGE.get(turn.get("role"))
        if message_cls is None:
            continue
        messages.append(message_cls(turn["content"]))
    return messages
