"""Stage 5 — Validate.

Takes each hypothesis from Stage 4 and asks the LLM (in a second pass) to
score how well it actually fits the code. Produces a confidence score in
[0.0, 1.0] for each hypothesis.

This file is named ``validate_stage.py`` (not ``validate.py``) to avoid
shadowing Pydantic's ``validate`` method.

Inputs : Hypotheses + RetrievedContext
Outputs: ScoredHypotheses

Implementation comes in W9.
"""

from __future__ import annotations

from .models import Hypotheses, RetrievedContext, ScoredHypotheses


def validate(hypotheses: Hypotheses, context: RetrievedContext) -> ScoredHypotheses:
    """Score each hypothesis against the actual code evidence.

    Args:
        hypotheses: The output of Stage 4.
        context: The code evidence from Stage 3 (re-used to ground scoring).

    Returns:
        ScoredHypotheses sorted by confidence descending.

    Raises:
        NotImplementedError: Until W9, when this stage is implemented.
    """
    raise NotImplementedError("Stage 5 (validate) — implementation lands in W9")
