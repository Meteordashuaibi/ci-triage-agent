"""Pipeline orchestrator.

Wires the 6 stages together in fixed sequential order:

    ingest → parse → retrieve → hypothesize → validate → plan

No branching, no retries here. Each stage's output feeds the next stage's
input. Pydantic enforces the contract at every boundary.

In later weeks this is where we'll add:
    - SQLite run-replay logging (W6)
    - Token / cost tracking (W6)
    - LLM caching (W12)
    - OpenTelemetry tracing (W11)
"""

from __future__ import annotations

from .hypothesize import hypothesize
from .ingest import ingest
from .models import RunRequest, TriageReport
from .parse import parse
from .plan import plan
from .retrieve import retrieve
from .validate_stage import validate


def run_pipeline(request: RunRequest) -> TriageReport:
    """Run the full 6-stage triage pipeline.

    Args:
        request: The repo + run_id to investigate.

    Returns:
        TriageReport with the final diagnostic output.
    """
    raw = ingest(request)
    parsed = parse(raw)
    context = retrieve(raw, parsed)
    hypotheses = hypothesize(parsed, context)
    scored = validate(hypotheses, context)
    report = plan(raw, parsed, scored)
    return report
