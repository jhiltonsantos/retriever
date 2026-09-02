import numpy as np

from app.config import GRAPH_MUTUAL_KNN_K
from app.dependencies import get_vectorstore
from app.services.materials import list_materials


def _fetch_chunks() -> dict:
    return get_vectorstore().get(include=["embeddings", "metadatas"])


def _normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    return matrix / norms


def build_materials_graph() -> dict:
    materials = list_materials()
    nodes = [
        {
            "id": material["id"],
            "label": material["title"] or material["source"],
            "source": material["source"],
            "type": material["type"],
            "chunk_count": material["chunk_count"],
        }
        for material in materials
    ]
    if not materials:
        return {"nodes": nodes, "edges": []}

    chunks = _fetch_chunks()
    embeddings = np.array(chunks["embeddings"]) if len(chunks["embeddings"]) else np.empty((0, 0))
    by_source: dict[str, list[int]] = {}
    for i, meta in enumerate(chunks["metadatas"]):
        by_source.setdefault(meta.get("source", ""), []).append(i)

    centroids: dict[str, np.ndarray] = {}
    for material in materials:
        idxs = by_source.get(material["source"], [])
        if idxs:
            centroids[material["id"]] = embeddings[idxs].mean(axis=0)

    edges = []
    ids = list(centroids.keys())
    if len(ids) >= 2:
        matrix = _normalize(np.array([centroids[i] for i in ids]))
        similarity = matrix @ matrix.T
        np.fill_diagonal(similarity, -1.0)

        # Similaridade de cosseno entre centroides de documento tem um piso alto
        # e uma faixa estreita (~0.6-0.98 no corpus real) -- nao existe um limiar
        # fixo que separe "mesmo assunto" de "assunto diferente", tudo fica acima
        # de qualquer corte razoavel. KNN mutuo resolve isso: um material so se
        # liga a outro se cada um estiver entre os K mais similares do outro,
        # o que reflete proximidade RELATIVA em vez de um valor absoluto.
        k = min(GRAPH_MUTUAL_KNN_K, len(ids) - 1)
        top_k = [set(np.argsort(-similarity[i])[:k]) for i in range(len(ids))]

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                score = float(similarity[i, j])
                strong = j in top_k[i] and i in top_k[j]
                edges.append({"source": ids[i], "target": ids[j], "weight": round(score, 4), "strong": strong})

    return {"nodes": nodes, "edges": edges}
