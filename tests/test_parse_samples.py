"""Temporary test file to generate failure types for Stage 2 development.

Will be removed once parse() is validated against all 4 failure types.
"""


def test_exception_failure() -> None:
    """Triggers a plain exception (not AssertionError)."""
    raise ValueError("intentional ValueError for Stage 2 parser validation")