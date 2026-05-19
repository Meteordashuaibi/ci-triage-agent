"""Eval runner — tests the parser against 48 real CI failures.

Metric: failure_type classification accuracy.
Ground truth was auto-labeled by the same parser, so this measures
consistency + regression detection, not absolute accuracy.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import Counter

# 让 Python 能找到 src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from src.models import RunRequest
from src.ingest import ingest
from src.parse import parse


def run_evals(cases_path: str = "evals/cases.json") -> None:
    with open(cases_path, encoding="utf-8") as f:
        cases = json.load(f)

    total = 0
    correct = 0
    wrong = []

    for i, case in enumerate(cases):
        ground_truth = case["ground_truth_failure_type"]
        if ground_truth in ("error", "timeout"):
            continue

        print(f"[{i+1}/{len(cases)}] {case['repo_url'].split('/')[-1]} run={case['run_id']}")

        try:
            raw = ingest(RunRequest(
                repo_url=case["repo_url"],
                run_id=case["run_id"],
            ))
            parsed = parse(raw)
            predicted = parsed.failure_type.value

            total += 1
            if predicted == ground_truth:
                correct += 1
                print(f"  ✅ {predicted}")
            else:
                wrong.append({
                    "repo": case["repo_url"],
                    "run_id": case["run_id"],
                    "ground_truth": ground_truth,
                    "predicted": predicted,
                })
                print(f"  ❌ predicted={predicted}, expected={ground_truth}")

        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {str(e)[:80]}")

    print()
    print("=" * 50)
    print(f"Total:   {total}")
    print(f"Correct: {correct}")
    print(f"Wrong:   {total - correct}")
    if total > 0:
        print(f"Accuracy: {correct/total:.1%}")

    if wrong:
        print()
        print("=== Wrong predictions ===")
        for w in wrong:
            print(f"  {w['repo'].split('/')[-1]} run={w['run_id']}")
            print(f"    expected={w['ground_truth']}, got={w['predicted']}")


if __name__ == "__main__":
    run_evals()