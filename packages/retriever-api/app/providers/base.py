from typing import Protocol, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel


class ModelInfo(TypedDict):
    id: str
    label: str


class TestResult(TypedDict):
    ok: bool
    reason: str | None
    message: str


class LlmProvider(Protocol):
    def build_llm(
        self, *, model: str | None, base_url: str, api_key: str | None
    ) -> BaseChatModel: ...

    def list_models(
        self, *, base_url: str, api_key: str | None
    ) -> list[ModelInfo]: ...

    def test_connection(
        self, *, model: str | None, base_url: str, api_key: str | None
    ) -> TestResult: ...

    def normalize_error(self, exc: Exception) -> Exception: ...


class ProviderConfigError(Exception):
    """Provedor remoto selecionado sem configuracao valida."""


class ProviderRequestError(Exception):
    """Provedor remoto falhou ao processar a requisicao."""
