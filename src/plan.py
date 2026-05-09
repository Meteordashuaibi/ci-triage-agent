"""Stage 6 — Plan.

Takes the scored hypotheses and produces the final, human-readable triage
report. Picks the top hypothesis, lists alternatives, and writes concrete
next steps.

This stage is intentionally human-in-the-loop: it does NOT modify code or
open PRs. It only produces a report for a developer to read.

Inputs : ParsedFailure + ScoredHypotheses
Outputs: TriageReport

Implementation comes in W10.
"""

from __future__ import annotations

from .models import ParsedFailure, RawRunData, ScoredHypotheses, TriageReport


def plan(
    raw: RawRunData,
    parsed: ParsedFailure,
    scored: ScoredHypotheses,
) -> TriageReport:
    """Build the final triage report.

    Args:
        raw: Used for repo_full_name and run_id metadata.
        parsed: Used for failure_type.
        scored: The ranked hypotheses to report.

    Returns:
        TriageReport ready to print to the CLI.

    Raises:
        NotImplementedError: Until W10, when this stage is implemented.
    """
    raise NotImplementedError("Stage 6 (plan) — implementation lands in W10")
