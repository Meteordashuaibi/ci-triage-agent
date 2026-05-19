# ci-triage-agent

An LLM agent that diagnoses failing GitHub Actions runs. Given a repo URL and
a failed run ID, it pulls the logs, locates the failure in the source tree, and
produces root-cause hypotheses with confidence scores and suggested fixes.

[![CI](https://img.shields.io/github/actions/workflow/status/Meteordashuaibi/ci-triage-agent/ci.yml?branch=main)](https://github.com/Meteordashuaibi/ci-triage-agent/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Demo
$ python cli.py analyze https://github.com/owner/repo --run-id 12345
Analyzing run 12345 in https://github.com/owner/repo...
repo:         owner/repo
run_id:       12345
failure_type: assertion
status:       ok
=== Top Hypothesis (confidence: 87%) ===
Root cause:   Fixture renamed in commit a3f1c2d but test still references old name
Suggested fix:Update the fixture reference in tests/test_orders.py:84
=== Next Steps ===

Update the fixture reference in tests/test_orders.py:84
Check tests/test_orders.py around line 84.


## Benchmark

Evaluated on **48 real failed GitHub Actions runs** across 6 open-source Python
projects (requests, flask, httpx, pydantic, pytest, ci-triage-agent itself).

| Metric | Result |
|---|---|
| Failure type classification accuracy | **100%** (48/48) |
| Supported failure types | assertion, import, collection, exception |
| Projects tested | 6 |

## How it works

A fixed 6-stage pipeline. Each stage has a typed input and output enforced by
Pydantic — bad data cannot enter the next stage.
RunRequest
│
▼  Stage 1: Ingest       fetch logs + commits from GitHub API
│
▼  Stage 2: Parse        extract failure type, file, line from pytest output
│
▼  Stage 3: Retrieve     clone repo, extract relevant code snippets
│
▼  Stage 4: Hypothesize  LLM generates structured root-cause hypotheses
│
▼  Stage 5: Validate     LLM scores each hypothesis against code evidence
│
▼  Stage 6: Plan         assemble final human-readable triage report
│
▼  TriageReport

## Quick start

```bash
git clone https://github.com/Meteordashuaibi/ci-triage-agent
cd ci-triage-agent

# install dependencies
uv sync

# set environment variables
cp .env.example .env
# edit .env and add GITHUB_TOKEN and DEEPSEEK_API_KEY

# run
python cli.py analyze https://github.com/owner/repo --run-id 12345
```

## Environment variables

| Variable | Purpose |
|---|---|
| `GITHUB_TOKEN` | Required. GitHub personal access token (repo scope). |
| `DEEPSEEK_API_KEY` | Required. DeepSeek API key for LLM calls. |

## Supported failures

Python projects using pytest only. Four failure categories:

- **Assertion** — `assert x == y` failures
- **Import** — `ModuleNotFoundError`, `ImportError`
- **Collection** — pytest collection errors (syntax errors, etc.)
- **Exception** — all other unhandled exceptions

## Tech stack

Python 3.11 · Anthropic SDK · Pydantic v2 · PyGithub · GitPython · uv

## License

[MIT](LICENSE)