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



def test_pipeline_fails_at_stage_two_not_stage_one() -> None:
    """Stage 1 is now implemented. Pipeline should get past ingest()
    and fail at Stage 2 (parse returns ok) then Stage 3 (retrieve)
    which still raises NotImplementedError."""
    request = RunRequest(
        repo_url="https://github.com/Meteordashuaibi/ci-triage-agent",
        run_id=26022017834,
    )
    with pytest.raises(NotImplementedError):
        run_pipeline(request)
def test_temporary_failure_for_stage3_testing() -> None:
    """Temporary: generates a fresh failed run for Stage 3 development."""
    assert 1 == 2, "intentional failure for Stage 3 testing"