from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from src.models import RunRequest
from src.ingest import ingest

raw = ingest(RunRequest(
    repo_url="https://github.com/Meteordashuaibi/ci-triage-agent",
    run_id=26027116480,
))

marker = "=== test/6_Run tests.txt ==="
start = raw.raw_logs.find(marker)
print(raw.raw_logs[start:start+3000])