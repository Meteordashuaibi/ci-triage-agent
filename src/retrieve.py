"""Stage 3 — Retrieve.

Finds code context relevant to the failure:
    - the failing file itself
    - the import chain (modules the failing file depends on)
    - recent commits that touched related files

Uses ripgrep + Python AST. No vector DB.

Inputs : RawRunData + ParsedFailure
Outputs: RetrievedContext

Implementation comes in W5.
"""

from __future__ import annotations

from .models import ParsedFailure, RawRunData, RetrievedContext


def retrieve(raw: RawRunData, parsed: ParsedFailure) -> RetrievedContext:
    """Retrieve code snippets and recent commits relevant to the failure.

    Args:
        raw: Output from Stage 1 (we still need workflow_yaml and recent_commits).
        parsed: Output from Stage 2 (tells us what to retrieve).

    Returns:
        RetrievedContext with snippets and relevant commits populated.

    Raises:
        NotImplementedError: Until W5, when this stage is implemented.
    """
    raise NotImplementedError("Stage 3 (retrieve) — implementation lands in W5")
