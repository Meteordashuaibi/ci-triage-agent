"""CI Triage Agent — command line interface.

Usage:
    ci-triage analyze <repo_url> --run-id <run_id>

Example:
    python cli.py analyze https://github.com/owner/repo --run-id 12345
"""

from __future__ import annotations

import argparse
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from src.models import RunRequest
from src.pipeline import run_pipeline


def cmd_analyze(args: argparse.Namespace) -> None:
    """Run the full triage pipeline and print the report."""
    request = RunRequest(
        repo_url=args.repo_url,
        run_id=args.run_id,
    )

    print(f"Analyzing run {args.run_id} in {args.repo_url}...")
    print()

    report = run_pipeline(request)

    print(f"repo:         {report.repo_full_name}")
    print(f"run_id:       {report.run_id}")
    print(f"failure_type: {report.failure_type.value}")
    print(f"status:       {report.status}")
    print()

    print(f"=== Top Hypothesis (confidence: {report.top_hypothesis.confidence:.0%}) ===")
    print(f"Root cause:   {report.top_hypothesis.hypothesis.root_cause}")
    print(f"Suggested fix:{report.top_hypothesis.hypothesis.suggested_fix}")
    print()

    print("=== Next Steps ===")
    for i, step in enumerate(report.next_steps, 1):
        print(f"  {i}. {step}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ci-triage",
        description="Analyze failed GitHub Actions runs with LLM",
    )
    subparsers = parser.add_subparsers(dest="command")

    # analyze subcommand
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a failed CI run")
    analyze_parser.add_argument("repo_url", help="GitHub repo URL")
    analyze_parser.add_argument("--run-id", type=int, required=True, help="Workflow run ID")

    args = parser.parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()