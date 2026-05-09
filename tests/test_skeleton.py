"""Skeleton tests — verify the *shape* of the pipeline, not behavior.

At W2 every stage raises NotImplementedError. These tests confirm that:
    1. All Pydantic models can be imported and instantiated.
    2. Every stage exists, accepts the right input type, and currently
       raises NotImplementedError (i.e. the contract is in place but the
       implementation is intentionally missing).

Real behavioral tests for each stage land alongside that stage's
implementation in later weeks.
"""

from __future__ import annotations

import pytest

from src.models import (
    FailureType,
    Hypotheses,
    Hypothesis,
    ParsedFailure,
    RawRunData,
    RetrievedContext,
    RunRequest,
    ScoredHypotheses,
    ScoredHypothesis,
)
from src.pipeline import run_pipeline


# ---------------------------------------------------------------------------
# Model contract tests — these MUST pass at all times.
# ---------------------------------------------------------------------------


def test_run_request_is_well_formed() -> None:
    request = RunRequest(
        repo_url="https://github.com/owner/repo",
        run_id=12345,
    )
    assert request.run_id == 12345


def test_failure_type_enum_has_four_supported_kinds() -> None:
    supported = {FailureType.ASSERTION, FailureType.IMPORT, FailureType.COLLECTION, FailureType.EXCEPTION}
    assert supported.issubset(set(FailureType))


def test_parsed_failure_accepts_minimal_fields() -> None:
    parsed = ParsedFailure(
        failure_type=FailureType.IMPORT,
        error_message="ModuleNotFoundError: No module named 'foo'",
    )
    assert parsed.failing_file is None  # optional


def test_scored_hypothesis_clamps_confidence_to_unit_interval() -> None:
    """confidence outside [0, 1] must be rejected by Pydantic."""
    valid = ScoredHypothesis(
        hypothesis=Hypothesis(
            root_cause="missing dependency",
            reasoning="the import line in foo.py refers to a package not in pyproject.toml",
            suggested_fix="add foo to dependencies",
        ),
        confidence=0.8,
        validation_notes="cited file matches the failing import",
    )
    assert valid.confidence == 0.8

    with pytest.raises(Exception):  # pydantic.ValidationError, but we don't care about the exact class here
        ScoredHypothesis(
            hypothesis=valid.hypothesis,
            confidence=1.5,  # out of range
            validation_notes="should fail validation",
        )


# ---------------------------------------------------------------------------
# Stage skeleton tests — confirm each stage exists and is wired into the
# pipeline, but is not yet implemented. These exist so that the moment a
# stage is implemented, removing the `NotImplementedError` test forces us
# to add a real behavioral test for it.
# ---------------------------------------------------------------------------


def test_pipeline_raises_not_implemented_at_stage_one() -> None:
    """Today, run_pipeline should fail at Stage 1 with NotImplementedError."""
    request = RunRequest(repo_url="https://github.com/owner/repo", run_id=1)
    with pytest.raises(NotImplementedError):
        run_pipeline(request)


def test_individual_stages_raise_not_implemented() -> None:
    """Each stage independently raises NotImplementedError until implemented."""
    from src.hypothesize import hypothesize
    from src.ingest import ingest
    from src.parse import parse
    from src.plan import plan
    from src.retrieve import retrieve
    from src.validate_stage import validate

    request = RunRequest(repo_url="https://github.com/owner/repo", run_id=1)

    # We construct dummy inputs just to confirm the type signatures match.
    # Each call should raise NotImplementedError before doing any real work.
    with pytest.raises(NotImplementedError):
        ingest(request)

    dummy_raw = RawRunData(
        repo_full_name="owner/repo",
        run_id=1,
        workflow_name="ci",
        head_sha="abc",
        raw_logs="",
        workflow_yaml="",
    )
    with pytest.raises(NotImplementedError):
        parse(dummy_raw)

    dummy_parsed = ParsedFailure(failure_type=FailureType.IMPORT, error_message="x")
    with pytest.raises(NotImplementedError):
        retrieve(dummy_raw, dummy_parsed)

    dummy_context = RetrievedContext(snippets=[])
    with pytest.raises(NotImplementedError):
        hypothesize(dummy_parsed, dummy_context)

    dummy_hypotheses = Hypotheses(hypotheses=[], model_used="none")
    with pytest.raises(NotImplementedError):
        validate(dummy_hypotheses, dummy_context)

    dummy_scored = ScoredHypotheses(scored=[])
    with pytest.raises(NotImplementedError):
        plan(dummy_raw, dummy_parsed, dummy_scored)
