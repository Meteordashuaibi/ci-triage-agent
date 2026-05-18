"""Stage 5 — Validate.

Takes each hypothesis from Stage 4 and asks the LLM to score
how well it fits the actual code evidence.

Inputs : Hypotheses + RetrievedContext
Outputs: ScoredHypotheses
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from .models import (
    Hypotheses,
    RetrievedContext,
    ScoredHypothesis,
    ScoredHypotheses,
)

load_dotenv(Path(__file__).parent.parent / ".env")

_CLIENT = Anthropic(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/anthropic",
)
MODEL = "deepseek-v4-flash"

SYSTEM_PROMPT = """You are an expert software engineer validating root cause hypotheses for CI failures.

Given a list of hypotheses and the actual code evidence, score each hypothesis.

You MUST respond with a JSON object in exactly this format:
{
  "scored": [
    {
      "index": 0,
      "confidence": 0.85,
      "validation_notes": "why this score"
    }
  ]
}

Rules:
- confidence is a float between 0.0 and 1.0
- 0.9+ means highly confident this is the root cause
- 0.5-0.9 means plausible but uncertain
- below 0.5 means unlikely
- validation_notes must cite specific evidence from the code
- respond with JSON only, no markdown, no explanation outside the JSON
"""


def _build_user_message(hypotheses: Hypotheses, context: RetrievedContext) -> str:
    """Build the validation prompt from hypotheses + code context."""
    parts = []

    parts.append("## Hypotheses to Validate")
    for i, h in enumerate(hypotheses.hypotheses):
        parts.append(f"\n### Hypothesis {i}")
        parts.append(f"Root cause: {h.root_cause}")
        parts.append(f"Reasoning: {h.reasoning}")
        parts.append(f"Suggested fix: {h.suggested_fix}")

    if context.snippets:
        parts.append("\n## Code Evidence")
        for snippet in context.snippets:
            parts.append(f"\n### {snippet.file_path} (lines {snippet.start_line}-{snippet.end_line})")
            parts.append(f"```python\n{snippet.content}\n```")

    return "\n".join(parts)


def validate(hypotheses: Hypotheses, context: RetrievedContext) -> ScoredHypotheses:
    """Score each hypothesis against the actual code evidence."""
    user_message = _build_user_message(hypotheses, context)

    response = _CLIENT.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = next(
        block.text for block in response.content if hasattr(block, "text")
    )

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    data = json.loads(raw)

    scored = []
    for item in data["scored"]:
        idx = item["index"]
        hypothesis = hypotheses.hypotheses[idx]
        scored.append(ScoredHypothesis(
            hypothesis=hypothesis,
            confidence=item["confidence"],
            validation_notes=item["validation_notes"],
        ))

    scored.sort(key=lambda x: x.confidence, reverse=True)

    return ScoredHypotheses(scored=scored)