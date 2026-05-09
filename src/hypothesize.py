"""Stage 4 — Hypothesize (the LLM core).

Sends the parsed failure + retrieved code context to an LLM and gets back
structured root cause hypotheses (Pydantic-enforced JSON output).

This is the most expensive stage in tokens and where most of the agent
"intelligence" lives. SQLite persistence and token tracking land here in W6.

Inputs : ParsedFailure + RetrievedContext
Outputs: Hypotheses

Implementation comes in W6.
"""

from __future__ import annotations

from .models import Hypotheses, ParsedFailure, RetrievedContext


def hypothesize(parsed: ParsedFailure, context: RetrievedContext) -> Hypotheses:
    """Ask the LLM for root cause hypotheses, with structured output.

    Args:
        parsed: The structured failure from Stage 2.
        context: The code evidence from Stage 3.

    Returns:
        Hypotheses containing one or more root cause candidates.

    Raises:
        NotImplementedError: Until W6, when this stage is implemented.
    """
    raise NotImplementedError("Stage 4 (hypothesize) — implementation lands in W6")
