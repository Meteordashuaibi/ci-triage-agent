"""Pydantic data models — the contracts between all 6 stages.

Each stage of the pipeline takes one of these as input and returns the next
one as output. Pydantic enforces the schema at every boundary, so a malformed
stage output cannot enter the next stage.

Pipeline data flow:

    RunRequest
        │
        ▼  Stage 1: ingest
    RawRunData
        │
        ▼  Stage 2: parse
    ParsedFailure
        │
        ▼  Stage 3: retrieve
    RetrievedContext
        │
        ▼  Stage 4: hypothesize
    Hypotheses
        │
        ▼  Stage 5: validate
    ScoredHypotheses
        │
        ▼  Stage 6: plan
    TriageReport
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Shared enums
# ---------------------------------------------------------------------------


class FailureType(str, Enum):
    """The 4 failure types this MVP supports.

    Anything outside this set is reported as ``UNSUPPORTED`` and the pipeline
    stops early with a clear message.
    """

    ASSERTION = "assertion"
    IMPORT = "import"
    COLLECTION = "collection"
    EXCEPTION = "exception"
    UNSUPPORTED = "unsupported"


# ---------------------------------------------------------------------------
# Stage 0: pipeline input
# ---------------------------------------------------------------------------


class RunRequest(BaseModel):
    """The user-facing input to the pipeline."""

    repo_url: str = Field(..., description="GitHub repo URL, e.g. https://github.com/owner/repo")
    run_id: int = Field(..., description="GitHub Actions workflow run ID")


# ---------------------------------------------------------------------------
# Stage 1: ingest output
# ---------------------------------------------------------------------------


class CommitInfo(BaseModel):
    """A single commit in the recent history of the repo."""

    sha: str
    author: str
    message: str
    timestamp: datetime
    files_changed: list[str] = Field(default_factory=list)


class RawRunData(BaseModel):
    """Everything Stage 1 pulls from GitHub before any parsing happens."""

    repo_full_name: str = Field(..., description="e.g. 'owner/repo'")
    run_id: int
    workflow_name: str
    head_sha: str
    raw_logs: str = Field(..., description="Concatenated stdout/stderr from the failed job")
    workflow_yaml: str = Field(..., description="Contents of the workflow YAML file")
    recent_commits: list[CommitInfo] = Field(
        default_factory=list,
        description="Most recent commits on the branch, newest first",
    )


# ---------------------------------------------------------------------------
# Stage 2: parse output
# ---------------------------------------------------------------------------


class ParsedFailure(BaseModel):
    """The structured representation of the failure extracted from raw logs."""

    failure_type: FailureType
    failing_file: str | None = Field(None, description="Path to the failing file, if identifiable")
    failing_line: int | None = Field(None, description="Line number of the failure, if identifiable")
    failing_test: str | None = Field(None, description="Pytest test ID, e.g. 'tests/test_x.py::test_y'")
    error_message: str = Field(..., description="The raw error/exception message")
    traceback: str | None = Field(None, description="Full Python traceback, if present")


# ---------------------------------------------------------------------------
# Stage 3: retrieve output
# ---------------------------------------------------------------------------


class CodeSnippet(BaseModel):
    """A single chunk of source code retrieved as evidence."""

    file_path: str
    start_line: int
    end_line: int
    content: str
    reason: str = Field(..., description="Why this snippet was retrieved (e.g. 'failing file', 'import chain')")


class RetrievedContext(BaseModel):
    """All the code context the LLM needs to form a hypothesis."""

    snippets: list[CodeSnippet]
    relevant_commits: list[CommitInfo] = Field(default_factory=list)
    total_tokens_estimate: int = Field(0, description="Rough token count, used to guard against context blow-up")


# ---------------------------------------------------------------------------
# Stage 4: hypothesize output
# ---------------------------------------------------------------------------


class Hypothesis(BaseModel):
    """A single LLM-generated root cause hypothesis."""

    root_cause: str = Field(..., description="One-sentence root cause statement")
    reasoning: str = Field(..., description="Why the LLM believes this; cites specific files/lines")
    suggested_fix: str = Field(..., description="High-level fix direction (no code edits applied)")


class Hypotheses(BaseModel):
    """All hypotheses from Stage 4, before validation."""

    hypotheses: list[Hypothesis]
    model_used: str
    input_tokens: int = 0
    output_tokens: int = 0


# ---------------------------------------------------------------------------
# Stage 5: validate output
# ---------------------------------------------------------------------------


class ScoredHypothesis(BaseModel):
    """A hypothesis with a confidence score after validation."""

    hypothesis: Hypothesis
    confidence: float = Field(..., ge=0.0, le=1.0, description="0.0–1.0 confidence score")
    validation_notes: str = Field(..., description="Why the score is what it is")


class ScoredHypotheses(BaseModel):
    """All hypotheses after Stage 5, sorted by confidence descending."""

    scored: list[ScoredHypothesis]


# ---------------------------------------------------------------------------
# Stage 6: plan output (final pipeline output)
# ---------------------------------------------------------------------------


class TriageReport(BaseModel):
    """The final, human-readable diagnostic report."""

    repo_full_name: str
    run_id: int
    failure_type: FailureType
    top_hypothesis: ScoredHypothesis
    alternative_hypotheses: list[ScoredHypothesis] = Field(default_factory=list)
    next_steps: list[str] = Field(..., description="Concrete actions the developer should take")
    status: Literal["ok", "low_confidence", "unsupported"] = "ok"
