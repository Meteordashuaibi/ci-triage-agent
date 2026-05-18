"""Stage 3 — Retrieve.

Clones the repo to a temp directory, then extracts code snippets
relevant to the failure found in Stage 2.

Inputs : RawRunData + ParsedFailure
Outputs: RetrievedContext
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import git
from dotenv import load_dotenv

from .models import CodeSnippet, ParsedFailure, RawRunData, RetrievedContext

load_dotenv(Path(__file__).parent.parent / ".env")

CONTEXT_WINDOW = 20  # lines before and after the failing line


def _clone_repo(repo_full_name: str) -> tempfile.TemporaryDirectory:
    """Clone the repo into a fresh temp directory and return it.

    The caller is responsible for calling .cleanup() when done.
    """
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://{token}@github.com/{repo_full_name}.git"
    tmp = tempfile.TemporaryDirectory()
    git.Repo.clone_from(url, tmp.name)
    return tmp


def _read_snippet(
    repo_dir: Path,
    relative_path: str,
    center_line: int,
    reason: str,
) -> CodeSnippet | None:
    """Read lines around center_line from a file in the cloned repo.

    Returns None if the file does not exist.
    """
    file_path = repo_dir / relative_path
    if not file_path.exists():
        return None

    lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(0, center_line - CONTEXT_WINDOW - 1)
    end = min(len(lines), center_line + CONTEXT_WINDOW)

    return CodeSnippet(
        file_path=relative_path,
        start_line=start + 1,
        end_line=end,
        content="\n".join(lines[start:end]),
        reason=reason,
    )


def retrieve(raw: RawRunData, parsed: ParsedFailure) -> RetrievedContext:
    """Retrieve code snippets relevant to the failure."""
    snippets: list[CodeSnippet] = []

    tmp = _clone_repo(raw.repo_full_name)
    try:
        repo_dir = Path(tmp.name)

        # Always retrieve the failing file if we know it
        if parsed.failing_file:
            line = parsed.failing_line or 1
            snippet = _read_snippet(
                repo_dir,
                parsed.failing_file,
                line,
                reason="failing file",
            )
            if snippet:
                snippets.append(snippet)

    finally:
        tmp.cleanup()

    total_tokens = sum(len(s.content.split()) * 2 for s in snippets)

    return RetrievedContext(
        snippets=snippets,
        relevant_commits=raw.recent_commits[:3],
        total_tokens_estimate=total_tokens,
    )