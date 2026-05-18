from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from src.models import RawRunData
from src.parse import parse

fake_logs = """
=== test/6_Run tests.txt ===
2026-05-18T10:00:00.000000Z ============================= test session starts ==============================
2026-05-18T10:00:00.000000Z collecting ... 
2026-05-18T10:00:00.000000Z ERROR collecting tests/test_bad_syntax.py
2026-05-18T10:00:00.000000Z E   SyntaxError: invalid syntax
2026-05-18T10:00:00.000000Z tests/test_bad_syntax.py:5: SyntaxError
2026-05-18T10:00:00.000000Z ========================= 1 error in 0.05s ==========================
"""

raw = RawRunData(
    repo_full_name="owner/repo",
    run_id=1,
    workflow_name="CI",
    head_sha="abc123",
    raw_logs=fake_logs,
    workflow_yaml="",
)

parsed = parse(raw)

print(f"failure_type: {parsed.failure_type}")
print(f"failing_file: {parsed.failing_file}")
print(f"failing_line: {parsed.failing_line}")
print(f"failing_test: {parsed.failing_test}")
print(f"error_message: {parsed.error_message[:100]}")