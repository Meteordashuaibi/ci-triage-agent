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

## 下一步
- 第 1 篇博客《Building a CI Failure Triage Agent: Why I'm Not Using LangChain》
  - 已经讨论过核心论点，但还没动笔
- Logfire 接入（SQLite tracing 已经够用，Logfire 可选）
- 第 2 项目（Battle Plan W14-15，8 月）
- 简历定稿（Battle Plan W16，8 月底）

## 项目配置
- 路径: D:\AAAubco\project\ci-triage-agent
- 环境: Windows 11 + PowerShell + .venv + uv
- Tech stack: Python 3.11, Pydantic v2, PyGithub, GitPython, Anthropic SDK
- LLM: DeepSeek V4 Flash via Anthropic-compatible API
- API keys in .env: GITHUB_TOKEN, DEEPSEEK_API_KEY
- SQLite DB: runs.db（tracing + caching 数据）

## 学到的关键概念（用于面试和博客）
- Pydantic 在 stage 边界做强制类型校验
- State machine 6 阶段 pipeline 设计：拆分 + 独立可测 + 出错可定位
- 手写 agent 而不用 LangChain：理解每一层 + 透明 + 好 debug
- 结构化输出：prompt 规定 JSON 格式 + json.loads + Pydantic 校验
- Caching：相同输入 hash 一致 → 直接返回缓存

## 已知问题（暂时不修）
- 某些大 repo (pandas/numpy) 日志太大，ingest 会超时
- Stage 2 的正则对复杂多 job CI 不够精确

## 重要提醒
- 红线：不学新框架、不投实习、不质疑方向、不做第 3 个项目
- 每周日休息
- 已经超前 Battle Plan 约三周