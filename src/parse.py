"""Stage 2 — Parse.

Extracts structured failure information from raw pytest logs:
    - failure type (one of 4 supported categories)
    - failing file + line number
    - failing test ID
    - error message and traceback

Inputs : RawRunData
Outputs: ParsedFailure

Implementation comes in W4.
"""

from __future__ import annotations

from .models import ParsedFailure, RawRunData


def parse(raw: RawRunData) -> ParsedFailure:
    """Parse pytest output into a structured failure record.

    Args:
        raw: The output from Stage 1 (ingest).

    Returns:
        ParsedFailure with failure_type, file, line, and traceback populated.

    Raises:
        NotImplementedError: Until W4, when this stage is implemented.
    """
    raise NotImplementedError("Stage 2 (parse) — implementation lands in W4")
