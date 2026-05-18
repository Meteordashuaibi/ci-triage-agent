"""Tests for Stage 2 — parse().

Uses fake log strings to test the parser in isolation,
without needing a real GitHub API call.
"""

from __future__ import annotations

import pytest
from src.models import FailureType, RawRunData
from src.parse import parse


def _make_raw(logs: str) -> RawRunData:
    """Helper: wrap a log string into a minimal RawRunData."""
    return RawRunData(
        repo_full_name="owner/repo",
        run_id=1,
        workflow_name="CI",
        head_sha="abc123",
        raw_logs=logs,
        workflow_yaml="",
    )


# ---------------------------------------------------------------
# ASSERTION
# ---------------------------------------------------------------

ASSERTION_LOG = """
=== test/6_Run tests.txt ===
2026-05-18T10:00:00.000000Z ============================= test session starts ==============================
2026-05-18T10:00:00.000000Z collected 1 item
2026-05-18T10:00:00.000000Z tests/test_foo.py::test_addition FAILED
2026-05-18T10:00:00.000000Z ================================== FAILURES ===================================
2026-05-18T10:00:00.000000Z     def test_addition():
2026-05-18T10:00:00.000000Z >       assert 1 + 1 == 3
2026-05-18T10:00:00.000000Z E       AssertionError: assert 2 == 3
2026-05-18T10:00:00.000000Z tests/test_foo.py:5: AssertionError
2026-05-18T10:00:00.000000Z ========================= 1 failed in 0.05s ==========================
"""


def test_parse_assertion_type() -> None:
    parsed = parse(_make_raw(ASSERTION_LOG))
    assert parsed.failure_type == FailureType.ASSERTION


def test_parse_assertion_file_and_line() -> None:
    parsed = parse(_make_raw(ASSERTION_LOG))
    assert parsed.failing_file == "tests/test_foo.py"
    assert parsed.failing_line == 5


def test_parse_assertion_test_name() -> None:
    parsed = parse(_make_raw(ASSERTION_LOG))
    assert parsed.failing_test == "tests/test_foo.py::test_addition"


# ---------------------------------------------------------------
# IMPORT
# ---------------------------------------------------------------

IMPORT_LOG = """
=== test/6_Run tests.txt ===
2026-05-18T10:00:00.000000Z ============================= test session starts ==============================
2026-05-18T10:00:00.000000Z collecting ...
2026-05-18T10:00:00.000000Z ERROR collecting tests/test_bar.py
2026-05-18T10:00:00.000000Z E   ModuleNotFoundError: No module named 'nonexistent_package'
2026-05-18T10:00:00.000000Z ========================= 1 error in 0.05s ==========================
"""


def test_parse_import_type() -> None:
    parsed = parse(_make_raw(IMPORT_LOG))
    assert parsed.failure_type == FailureType.IMPORT


def test_parse_import_no_file_or_line() -> None:
    """Import errors happen before any test runs, so file/line are None."""
    parsed = parse(_make_raw(IMPORT_LOG))
    assert parsed.failing_file is None
    assert parsed.failing_line is None


# ---------------------------------------------------------------
# COLLECTION
# ---------------------------------------------------------------

COLLECTION_LOG = """
=== test/6_Run tests.txt ===
2026-05-18T10:00:00.000000Z ============================= test session starts ==============================
2026-05-18T10:00:00.000000Z collecting ...
2026-05-18T10:00:00.000000Z ERROR collecting tests/test_bad_syntax.py
2026-05-18T10:00:00.000000Z E   SyntaxError: invalid syntax
2026-05-18T10:00:00.000000Z tests/test_bad_syntax.py:5: SyntaxError
2026-05-18T10:00:00.000000Z ========================= 1 error in 0.05s ==========================
"""


def test_parse_collection_type() -> None:
    parsed = parse(_make_raw(COLLECTION_LOG))
    assert parsed.failure_type == FailureType.COLLECTION


def test_parse_collection_file_and_line() -> None:
    parsed = parse(_make_raw(COLLECTION_LOG))
    assert parsed.failing_file == "tests/test_bad_syntax.py"
    assert parsed.failing_line == 5


# ---------------------------------------------------------------
# EXCEPTION
# ---------------------------------------------------------------

EXCEPTION_LOG = """
=== test/6_Run tests.txt ===
2026-05-18T10:00:00.000000Z ============================= test session starts ==============================
2026-05-18T10:00:00.000000Z collected 1 item
2026-05-18T10:00:00.000000Z tests/test_parse_samples.py::test_exception_failure FAILED
2026-05-18T10:00:00.000000Z ================================== FAILURES ===================================
2026-05-18T10:00:00.000000Z     def test_exception_failure():
2026-05-18T10:00:00.000000Z >       raise ValueError("intentional ValueError")
2026-05-18T10:00:00.000000Z E       ValueError: intentional ValueError
2026-05-18T10:00:00.000000Z tests/test_parse_samples.py:9: ValueError
2026-05-18T10:00:00.000000Z ========================= 1 failed in 0.05s ==========================
"""


def test_parse_exception_type() -> None:
    parsed = parse(_make_raw(EXCEPTION_LOG))
    assert parsed.failure_type == FailureType.EXCEPTION


def test_parse_exception_file_and_line() -> None:
    parsed = parse(_make_raw(EXCEPTION_LOG))
    assert parsed.failing_file == "tests/test_parse_samples.py"
    assert parsed.failing_line == 9


# ---------------------------------------------------------------
# UNSUPPORTED
# ---------------------------------------------------------------

UNSUPPORTED_LOG = """
=== test/6_Run tests.txt ===
2026-05-18T10:00:00.000000Z build failed: unknown reason
"""


def test_parse_unsupported_type() -> None:
    parsed = parse(_make_raw(UNSUPPORTED_LOG))
    assert parsed.failure_type == FailureType.UNSUPPORTED