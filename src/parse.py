"""Stage 2 — Parse.

Extracts structured failure information from raw pytest logs.

Inputs : RawRunData
Outputs: ParsedFailure
"""

from __future__ import annotations

import re

from .models import FailureType, ParsedFailure, RawRunData


# 时间戳前缀，每行日志都有，解析时要去掉
# 格式: 2026-05-18T08:23:49.1234567Z
_TIMESTAMP = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z "


def _strip_timestamp(line: str) -> str:
    """去掉每行开头的时间戳，返回实际内容。"""
    return re.sub(_TIMESTAMP, "", line)


def _detect_failure_type(logs: str) -> FailureType:
    """从日志里判断是哪种失败类型。"""
    if re.search(r"AssertionError", logs):
        return FailureType.ASSERTION
    if re.search(r"ImportError|ModuleNotFoundError", logs):
        return FailureType.IMPORT
    if re.search(r"ERROR collecting", logs):
        return FailureType.COLLECTION
    if re.search(r"Exception|Error", logs):
        return FailureType.EXCEPTION
    return FailureType.UNSUPPORTED


def _extract_failing_location(logs: str) -> tuple[str | None, int | None, str | None]:
    """提取失败的文件、行号、测试名。

    pytest 失败时会输出这样的行:
        tests/test_foo.py:42: AssertionError
    """
    pattern = r"([\w/\\.-]+\.py):(\d+): \w+Error"
    match = re.search(pattern, logs)
    if not match:
        return None, None, None

    failing_file = match.group(1)
    failing_line = int(match.group(2))

# 找 FAILED 那一行，格式: tests/foo.py::test_bar FAILED
    test_pattern = rf"([\w/\\.-]+\.py)::([\w\[\]-]+) FAILED"
    test_match = re.search(test_pattern, logs)
    failing_test = f"{test_match.group(1)}::{test_match.group(2)}" if test_match else None

    return failing_file, failing_line, failing_test


def _extract_error_message(logs: str) -> str:
    """提取报错信息，就是日志里 'E  ' 开头的那些行。"""
    lines = logs.splitlines()
    error_lines = []
    for line in lines:
        cleaned = _strip_timestamp(line)
        if cleaned.startswith("E "):
            error_lines.append(cleaned.lstrip("E ").strip())
    return "\n".join(error_lines) if error_lines else "unknown error"


def parse(raw: RawRunData) -> ParsedFailure:
    """Parse pytest output into a structured failure record."""
    logs = raw.raw_logs

    failure_type = _detect_failure_type(logs)
    failing_file, failing_line, failing_test = _extract_failing_location(logs)
    error_message = _extract_error_message(logs)

    return ParsedFailure(
        failure_type=failure_type,
        failing_file=failing_file,
        failing_line=failing_line,
        failing_test=failing_test,
        error_message=error_message,
        traceback=None,
    )