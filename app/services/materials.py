from datetime import datetime, timezone
from uuid import uuid4

from app.db import get_connection


def list_materials() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, source, type, title, chunk_count, ingested_at FROM materials ORDER BY ingested_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def record_material(source: str, type: str, title: str, chunk_count: int) -> dict:
    material_id = uuid4().hex
    ingested_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO materials (id, source, type, title, chunk_count, ingested_at) VALUES (?, ?, ?, ?, ?, ?)",
            (material_id, source, type, title, chunk_count, ingested_at),
        )
    return {
        "id": material_id,
        "source": source,
        "type": type,
        "title": title,
        "chunk_count": chunk_count,
        "ingested_at": ingested_at,
    }


def delete_material(material_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM materials WHERE id = ?", (material_id,))
    return cursor.rowcount > 0
