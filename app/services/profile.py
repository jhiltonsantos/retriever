from datetime import datetime, timezone

from app.db import get_connection


def get_profile() -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, display_name, created_at, updated_at FROM user_profile WHERE id = 1"
        ).fetchone()
        if row is None:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO user_profile (id, display_name, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (1, None, now, now),
            )
            row = conn.execute(
                "SELECT id, display_name, created_at, updated_at FROM user_profile WHERE id = 1"
                
            ).fetchone()
    return dict(row)


def update_profile(display_name: str | None) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO user_profile (id, display_name, created_at, updated_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 display_name = excluded.display_name,
                 updated_at = excluded.updated_at""",
            (1, display_name, now, now),
        )
        row = conn.execute(
            "SELECT id, display_name, created_at, updated_at FROM user_profile WHERE id = 1"
        ).fetchone()
    return dict(row)
