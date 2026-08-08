import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from app.config import LLM_API_KEY, LLM_PROVIDER, SETTINGS_DIR

DB_PATH = SETTINGS_DIR / "retriever.db"
LEGACY_SETTINGS_FILE = SETTINGS_DIR / "settings.json"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS llm_provider_settings (
    provider TEXT PRIMARY KEY,
    model TEXT,
    base_url TEXT,
    api_key TEXT,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    display_name TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    sources TEXT,
    agent_steps TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS materials (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('pdf', 'text')),
    title TEXT,
    chunk_count INTEGER NOT NULL DEFAULT 0,
    ingested_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_materials_source ON materials(source);
"""


@contextmanager
def get_connection():
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    is_new = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA_SQL)
        if is_new:
            os.chmod(DB_PATH, 0o600)
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Chamada uma vez pelo lifespan da app. Garante o schema e migra o
    settings.json legado para o SQLite, se aplicavel."""
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM llm_provider_settings").fetchone()
        if row["n"] == 0 and LEGACY_SETTINGS_FILE.exists():
            _migrate_legacy_settings(conn)


def _migrate_legacy_settings(conn: sqlite3.Connection) -> None:
    from app.settings_store import default_base_url  # import local: evita ciclo de import no load do modulo

    saved = json.loads(LEGACY_SETTINGS_FILE.read_text())
    provider = saved.get("provider") or LLM_PROVIDER
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO llm_provider_settings (provider, model, base_url, api_key, updated_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(provider) DO UPDATE SET
             model=excluded.model, base_url=excluded.base_url,
             api_key=excluded.api_key, updated_at=excluded.updated_at""",
        (
            provider,
            saved.get("model"),
            saved.get("base_url") or default_base_url(provider),
            saved.get("api_key") or (LLM_API_KEY or None),
            now,
        ),
    )
    conn.execute(
        """INSERT INTO app_settings (key, value) VALUES ('active_llm_provider', ?)
           ON CONFLICT(key) DO UPDATE SET value = excluded.value""",
        (provider,),
    )
    LEGACY_SETTINGS_FILE.rename(LEGACY_SETTINGS_FILE.parent / (LEGACY_SETTINGS_FILE.name + ".bak"))
