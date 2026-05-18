"""Stage 6 — Plan.

Assembles the final triage report from scored hypotheses.
No LLM call here — just organizing the results.

Inputs : RawRunData + ParsedFailure + ScoredHypotheses
Outputs: TriageReport
"""

from __future__ import annotations

from .models import (
    FailureType,
    ParsedFailure,
    RawRunData,
    ScoredHypotheses,
    TriageReport,
)

CONFIDENCE_THRESHOLD = 0.4


def plan(
    raw: RawRunData,
    parsed: ParsedFailure,
    scored: ScoredHypotheses,
) -> TriageReport:
    """Build the final triage report."""

    # 没有任何假设，或者失败类型不支持
    if not scored.scored or parsed.failure_type == FailureType.UNSUPPORTED:
        return TriageReport(
            repo_full_name=raw.repo_full_name,
            run_id=raw.run_id,
            failure_type=parsed.failure_type,
            top_hypothesis=scored.scored[0] if scored.scored else None,
            alternative_hypotheses=[],
            next_steps=["Failure type is not supported by this tool."],
            status="unsupported",
        )

    top = scored.scored[0]
    alternatives = scored.scored[1:]

    # 置信度太低，说明 LLM 也不确定
    if top.confidence < CONFIDENCE_THRESHOLD:
        status = "low_confidence"
        next_steps = [
            f"Low confidence ({top.confidence:.0%}) — manual investigation recommended.",
            f"Most likely cause: {top.hypothesis.root_cause}",
            top.hypothesis.suggested_fix,
        ]
    else:
        status = "ok"
        next_steps = [
            top.hypothesis.suggested_fix,
            f"Check {parsed.failing_file} around line {parsed.failing_line}.",
        ]

    return TriageReport(
        repo_full_name=raw.repo_full_name,
        run_id=raw.run_id,
        failure_type=parsed.failure_type,
        top_hypothesis=top,
        alternative_hypotheses=alternatives,
        next_steps=next_steps,
        status=status,
    )