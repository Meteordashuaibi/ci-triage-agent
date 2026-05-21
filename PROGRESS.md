# Progress Log

## Project
CI Failure Triage Agent — LLM agent that analyzes failed GitHub Actions runs.
GitHub repo: https://github.com/Meteordashuaibi/ci-triage-agent

## Completed (按 Battle Plan 周次)
- W1: 5 个 practice demo ✅
- W2: 项目骨架 + Pydantic 模型 + CI ✅
- W3: Stage 1 (ingest) — GitHub API 拉日志/commits ✅
- W4: Stage 2 (parse) — 正则提取失败类型/文件/行号 + 10 个单元测试 ✅
- W5: Stage 3 (retrieve) — clone repo + 代码片段提取 + 边界 bug 修复 ✅
- W6: Stage 4 (hypothesize) — LLM 生成结构化根因假设 ✅
- W9: Stage 5 (validate) — LLM 二次评分置信度 ✅
- W10: Stage 6 (plan) + CLI（ci-triage analyze）✅
- W11: Eval 套件 — 48 cases，failure_type 准确率 100% ✅
- W11: SQLite tracing — 每个 stage 耗时 + token 用量 ✅
- W12: LLM response caching — hash-keyed，cache HIT 时 Stage 4 从 9s → 0s ✅
- README v2 — benchmark + quickstart + demo output ✅

## 项目配置
- 路径: D:\AAAubco\project\ci-triage-agent
- 环境: Windows 11 + PowerShell + .venv + uv
- Tech stack: Python 3.11, Pydantic v2, PyGithub, GitPython, Anthropic SDK
- LLM: DeepSeek V4 Flash via Anthropic-compatible API
- API keys in .env: GITHUB_TOKEN, DEEPSEEK_API_KEY
- SQLite DB: runs.db（tracing + caching 数据）
