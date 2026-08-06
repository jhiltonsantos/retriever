from typing import Protocol

from langchain_core.language_models.chat_models import BaseChatModel


class LlmProvider(Protocol):
    def build_llm(self) -> BaseChatModel: ...

    def normalize_error(self, exc: Exception) -> Exception: ...


class ProviderConfigError(Exception):
    """Provedor remoto selecionado sem configuracao valida."""


class ProviderRequestError(Exception):
    """Provedor remoto falhou ao processar a requisicao."""
