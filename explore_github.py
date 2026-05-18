from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from src.models import RunRequest
from src.ingest import ingest

test_cases = [
    ("https://github.com/psf/requests", 25747498310),
    ("https://github.com/pallets/flask", 25964629914),
    ("https://github.com/encode/httpx", 22547825202),
    ("https://github.com/pydantic/pydantic", 26019401861),
]

for repo_url, run_id in test_cases:
    print(f"测试: {repo_url}")
    try:
        result = ingest(RunRequest(repo_url=repo_url, run_id=run_id))
        print(f"  ✅ repo={result.repo_full_name}, logs={len(result.raw_logs)}字符, commits={len(result.recent_commits)}")
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {e}")
    print()