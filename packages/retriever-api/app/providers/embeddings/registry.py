from app.providers.embeddings.base import EmbeddingsProvider
from app.providers.embeddings.ollama import OllamaEmbeddingsProvider

_PROVIDERS: dict[str, EmbeddingsProvider] = {
    "ollama": OllamaEmbeddingsProvider(),
}


def get_embeddings_provider(name: str) -> EmbeddingsProvider:
    try:
        return _PROVIDERS[name]
    except KeyError:
        raise ValueError(
            f"EMBED_PROVIDER invalido: {name!r}. Use um destes: {', '.join(_PROVIDERS)}."
        ) from None
