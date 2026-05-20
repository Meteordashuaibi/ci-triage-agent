"""Stage 4 — Hypothesize.

Sends parsed failure + retrieved code context to an LLM and gets back
structured root cause hypotheses.

Inputs : ParsedFailure + RetrievedContext
Outputs: Hypotheses
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from .models import Hypotheses, Hypothesis, ParsedFailure, RetrievedContext

load_dotenv(Path(__file__).parent.parent / ".env")

_CLIENT = Anthropic(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/anthropic",
)
MODEL = "deepseek-v4-flash"

SYSTEM_PROMPT = """You are an expert software engineer specializing in diagnosing CI failures.

Given a failed pytest run, analyze the failure and produce root cause hypotheses.

You MUST respond with a JSON object in exactly this format:
{
  "hypotheses": [
    {
      "root_cause": "one sentence describing the root cause",
      "reasoning": "why you believe this, citing specific files and line numbers",
      "suggested_fix": "high-level fix direction, no code changes"
    }
  ]
}

Rules:
- Produce 1-3 hypotheses, most likely first
- Be specific: cite file names and line numbers
- Do NOT suggest running tests or checking logs (the user already has them)
- Respond with JSON only, no markdown, no explanation outside the JSON
"""


def _build_user_message(parsed: ParsedFailure, context: RetrievedContext) -> str:
    """Build the user message from parsed failure + code context."""
    parts = []

    parts.append("## Failure Summary")
    parts.append(f"- Type: {parsed.failure_type.value}")
    parts.append(f"- File: {parsed.failing_file}")
    parts.append(f"- Line: {parsed.failing_line}")
    parts.append(f"- Test: {parsed.failing_test}")
    parts.append(f"- Error: {parsed.error_message}")

    if context.snippets:
        parts.append("\n## Relevant Code")
        for snippet in context.snippets:
            parts.append(f"\n### {snippet.file_path} (lines {snippet.start_line}-{snippet.end_line})")
            parts.append(f"Reason: {snippet.reason}")
            parts.append(f"```python\n{snippet.content}\n```")

    if context.relevant_commits:
        parts.append("\n## Recent Commits")
        for commit in context.relevant_commits:
            parts.append(f"- {commit.sha[:7]} {commit.author}: {commit.message.splitlines()[0]}")

    return "\n".join(parts)


def hypothesize(parsed: ParsedFailure, context: RetrievedContext) -> Hypotheses:
    """Ask the LLM for root cause hypotheses."""
    user_message = _build_user_message(parsed, context)

    from .cache import get_cached, set_cached

    cached = get_cached(SYSTEM_PROMPT, user_message)
    if cached:
        raw = cached
        input_tokens = 0
        output_tokens = 0
    else:
        response = _CLIENT.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = next(
            block.text for block in response.content if hasattr(block, "text")
        )
        set_cached(SYSTEM_PROMPT, user_message, raw, MODEL)
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    data = json.loads(raw)
    hypotheses = [Hypothesis(**h) for h in data["hypotheses"]]

    return Hypotheses(
        hypotheses=hypotheses,
        model_used=MODEL,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )