"""Stage 1 — Ingest.

Pulls everything we need from GitHub before any analysis happens:
    - failed workflow run logs
    - workflow YAML
    - recent commits on the branch

Inputs : RunRequest
Outputs: RawRunData
"""

from __future__ import annotations

import io
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from github import Auth, Github
import os

from .models import CommitInfo, RawRunData, RunRequest

load_dotenv(Path(__file__).parent.parent / ".env")


def _get_client() -> Github:
    """初始化 PyGithub 客户端，用 .env 里的 GITHUB_TOKEN。"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN 未设置，请检查 .env 文件")
    return Github(auth=Auth.Token(token))


def _download_logs(run, token: str) -> str:
    """下载 workflow run 的日志 zip，返回所有 step 日志拼接的字符串。"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(run.logs_url, headers=headers, allow_redirects=True)
    response.raise_for_status()

    z = zipfile.ZipFile(io.BytesIO(response.content))
    parts = []
    for name in z.namelist():
        content = z.read(name).decode("utf-8", errors="replace")
        parts.append(f"=== {name} ===\n{content}")
    return "\n".join(parts)


def _get_recent_commits(repo, head_sha: str, limit: int = 10) -> list[CommitInfo]:
    """拿最近 limit 条 commits。"""
    commits = []
    for commit in repo.get_commits(sha=head_sha)[:limit]:
        commits.append(CommitInfo(
            sha=commit.sha,
            author=commit.commit.author.name,
            message=commit.commit.message,
            timestamp=commit.commit.author.date.replace(tzinfo=timezone.utc),
            files_changed=[f.filename for f in commit.files],
        ))
    return commits


def ingest(request: RunRequest) -> RawRunData:
    """Fetch raw run data from GitHub."""
    g = _get_client()
    token = os.getenv("GITHUB_TOKEN")

    # repo_url 格式: https://github.com/owner/repo
    repo_name = "/".join(request.repo_url.rstrip("/").split("/")[-2:])
    repo = g.get_repo(repo_name)

    run = repo.get_workflow_run(request.run_id)

    logs = _download_logs(run, token)
    commits = _get_recent_commits(repo, run.head_sha)

    return RawRunData(
        repo_full_name=repo.full_name,
        run_id=run.id,
        workflow_name=run.name,
        head_sha=run.head_sha,
        raw_logs=logs,
        workflow_yaml="",  # W3 では後で実装
        recent_commits=commits,
    )