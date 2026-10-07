from typing import Protocol, TypedDict

from langchain_core.embeddings import Embeddings


class EmbeddingsStatus(TypedDict):
    # "ready" | "model_missing" | "unreachable" - ver docs/api-contract.md
    status: str


class EmbeddingsProvider(Protocol):
    def build(self, *, model: str, base_url: str) -> Embeddings: ...

    def check_status(self, *, model: str, base_url: str) -> EmbeddingsStatus: ...
