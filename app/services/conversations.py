import json
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from app.db import get_connection


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def list_conversations() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_conversation(conversation_id: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
        if row is None:
            return None

        messages = conn.execute(
            "SELECT id, role, content, sources, agent_steps, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,),
        ).fetchall()

    conversation = dict(row)
    conversation["messages"] = [_message_row_to_dict(m) for m in messages]
    return conversation


def create_conversation(title: str) -> dict:
    conversation_id = uuid4().hex
    now = _now()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conversation_id, title, now, now),
        )
    return {"id": conversation_id, "title": title, "created_at": now, "updated_at": now}


def delete_conversation(conversation_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM conversations WHERE id = ?", (conversation_id,)
        )
    return cursor.rowcount > 0


def add_message(
    conversation_id: str,
    role: str,
    content: str,
    sources: list | None = None,
    agent_steps: list | None = None,
) -> dict:
    message_id = uuid4().hex
    now = _now()
    sources_json = json.dumps(sources) if sources is not None else None
    steps_json = json.dumps(agent_steps) if agent_steps is not None else None

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (id, conversation_id, role, content, sources, agent_steps, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (message_id, conversation_id, role, content, sources_json, steps_json, now),
        )
        conn.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, conversation_id),
        )

    return {
        "id": message_id,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "sources": sources,
        "agent_steps": agent_steps,
        "created_at": now,
    }


def update_conversation_title(conversation_id: str, title: str) -> dict | None:
    now = _now()
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, now, conversation_id),
        )
        if cursor.rowcount == 0:
            return None
        row = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
    return dict(row)


def _message_row_to_dict(row: sqlite3.Row) -> dict:  # type: ignore[name-defined]
    data = dict(row)
    data["sources"] = json.loads(data["sources"]) if data["sources"] is not None else None
    data["agent_steps"] = json.loads(data["agent_steps"]) if data["agent_steps"] is not None else None
    return data
