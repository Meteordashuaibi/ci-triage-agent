"""Simple SQLite-based tracer for pipeline runs.

Records timing and token usage for each pipeline execution.
"""

from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "runs.db"


def _get_conn() -> sqlite3.Connection:
    """Get a SQLite connection, creating the DB and tables if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_full_name TEXT,
            run_id INTEGER,
            failure_type TEXT,
            status TEXT,
            total_seconds REAL,
            input_tokens INTEGER,
            output_tokens INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stage_timings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_db_id INTEGER,
            stage_name TEXT,
            seconds REAL,
            FOREIGN KEY (run_db_id) REFERENCES runs(id)
        )
    """)
    conn.commit()
    return conn


class RunTracer:
    """Tracks timing and metadata for a single pipeline run."""

    def __init__(self, repo_full_name: str, run_id: int) -> None:
        self.repo_full_name = repo_full_name
        self.run_id = run_id
        self._stage_timings: dict[str, float] = {}
        self._start = time.time()
        self._input_tokens = 0
        self._output_tokens = 0

    @contextmanager
    def stage(self, name: str):
        """Context manager to time a single stage."""
        t0 = time.time()
        print(f"  [{name}] running...")
        try:
            yield
        finally:
            elapsed = time.time() - t0
            self._stage_timings[name] = elapsed
            print(f"  [{name}] done in {elapsed:.2f}s")

    def add_tokens(self, input_tokens: int, output_tokens: int) -> None:
        """Record LLM token usage."""
        self._input_tokens += input_tokens
        self._output_tokens += output_tokens

    def save(self, failure_type: str, status: str) -> None:
        """Save the run record to SQLite."""
        total = time.time() - self._start
        conn = _get_conn()
        cursor = conn.execute(
            """INSERT INTO runs
               (repo_full_name, run_id, failure_type, status,
                total_seconds, input_tokens, output_tokens)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (self.repo_full_name, self.run_id, failure_type,
             status, total, self._input_tokens, self._output_tokens),
        )
        run_db_id = cursor.lastrowid
        for stage_name, seconds in self._stage_timings.items():
            conn.execute(
                "INSERT INTO stage_timings (run_db_id, stage_name, seconds) VALUES (?, ?, ?)",
                (run_db_id, stage_name, seconds),
            )
        conn.commit()
        conn.close()
        print(f"\n  Total: {total:.2f}s | "
              f"tokens: {self._input_tokens}in / {self._output_tokens}out")
        print(f"  Saved to runs.db (run_db_id={run_db_id})")