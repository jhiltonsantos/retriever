from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import OllamaEmbeddings

from app.config import CHROMA_DIR, EMBED_MODEL, OLLAMA_BASE_URL, RETRIEVER_K
from app.prompts.tutor import tutor_prompt
from app.providers.registry import get_provider

_embeddings = None
_vectorstore = None
_llm = None
_retrieval_chain = None


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
        _llm = get_provider().build_llm()
    return _llm


def get_retrieval_chain():
    global _retrieval_chain
    if _retrieval_chain is None:
        llm = get_llm()
        retriever = get_vectorstore().as_retriever(
            search_kwargs={"k": RETRIEVER_K},
        )
        combine_docs_chain = create_stuff_documents_chain(llm, tutor_prompt)
        _retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    return _retrieval_chain
