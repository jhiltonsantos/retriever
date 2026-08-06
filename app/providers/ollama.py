from langchain_ollama import ChatOllama

from app.config import LLM_MODEL, OLLAMA_BASE_URL

DEFAULT_MODEL = "llama3"


class OllamaProvider:
    def build_llm(self) -> ChatOllama:
        return ChatOllama(model=LLM_MODEL or DEFAULT_MODEL, base_url=OLLAMA_BASE_URL)

    def normalize_error(self, exc: Exception) -> Exception:
        return exc
