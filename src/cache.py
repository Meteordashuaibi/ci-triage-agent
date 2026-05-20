"""LLM response cache backed by SQLite.

Uses a hash of the prompt as the cache key.
Same input → same output, no LLM call needed.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "runs.db"


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS llm_cache (
            prompt_hash TEXT PRIMARY KEY,
            response TEXT,
            model TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


def _hash_prompt(system: str, user: str) -> str:
    """Compute a stable hash from system + user prompt."""
    content = f"{system}\n\n{user}"
    return hashlib.sha256(content.encode()).hexdigest()


def get_cached(system: str, user: str) -> str | None:
    """Return cached response if available, else None."""
    key = _hash_prompt(system, user)
    conn = _get_conn()
    row = conn.execute(
        "SELECT response FROM llm_cache WHERE prompt_hash = ?", (key,)
    ).fetchone()
    conn.close()
    if row:
        print("  [cache] HIT")
        return row[0]
    print("  [cache] MISS — calling LLM")
    return None


def set_cached(system: str, user: str, response: str, model: str) -> None:
    """Store a response in the cache."""
    key = _hash_prompt(system, user)
    conn = _get_conn()
    conn.execute(
        """INSERT OR REPLACE INTO llm_cache
           (prompt_hash, response, model) VALUES (?, ?, ?)""",
        (key, response, model),
    )
    conn.commit()
    conn.close()