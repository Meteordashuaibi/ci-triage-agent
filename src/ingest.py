"""Stage 1 — Ingest.

Pulls everything we need from GitHub before any analysis happens:
    - failed workflow run logs
    - workflow YAML
    - recent commits on the branch

Inputs : RunRequest
Outputs: RawRunData

Implementation comes in W3.
"""

from __future__ import annotations

from .models import RawRunData, RunRequest


def ingest(request: RunRequest) -> RawRunData:
    """Fetch raw run data from GitHub.

    Args:
        request: The repo + run_id to investigate.

    Returns:
        RawRunData with logs, workflow YAML, and recent commits populated.

    Raises:
        NotImplementedError: Until W3, when this stage is implemented.
    """
    raise NotImplementedError("Stage 1 (ingest) — implementation lands in W3")
