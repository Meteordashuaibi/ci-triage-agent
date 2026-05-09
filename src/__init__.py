"""ci-triage-agent — LLM agent that analyzes failed GitHub Actions runs.

Public API: import what you need from the top level.
"""

from .models import (
    CodeSnippet,
    CommitInfo,
    FailureType,
    Hypotheses,
    Hypothesis,
    ParsedFailure,
    RawRunData,
    RetrievedContext,
    RunRequest,
    ScoredHypotheses,
    ScoredHypothesis,
    TriageReport,
)
from .pipeline import run_pipeline

__all__ = [
    "CodeSnippet",
    "CommitInfo",
    "FailureType",
    "Hypotheses",
    "Hypothesis",
    "ParsedFailure",
    "RawRunData",
    "RetrievedContext",
    "RunRequest",
    "ScoredHypotheses",
    "ScoredHypothesis",
    "TriageReport",
    "run_pipeline",
]
