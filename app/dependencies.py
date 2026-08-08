from langchain_chroma import Chroma
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import OllamaEmbeddings

from app.config import CHROMA_DIR, EMBED_MODEL, OLLAMA_BASE_URL
from app.providers.registry import get_provider
from app.settings_store import get_effective_config

_embeddings = None
_vectorstore = None
_llm = None
_agent_graph = None


def get_embeddings() -> OllamaEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = OllamaEmbeddings(
            model=EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
    return _embeddings


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _vectorstore = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=get_embeddings(),
        )
    return _vectorstore


def get_llm() -> BaseChatModel:
    global _llm
    if _llm is None:
        cfg = get_effective_config()
        _llm = get_provider(cfg.provider).build_llm(
            model=cfg.model, base_url=cfg.base_url, api_key=cfg.api_key
        )
    return _llm


def get_agent_graph():
    global _agent_graph
    if _agent_graph is None:
        from app.graph.rag_agent import build_graph

        _agent_graph = build_graph().compile()
    return _agent_graph


def reset_llm_cache() -> None:
    global _llm
    _llm = None
