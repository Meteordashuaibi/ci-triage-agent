# Progress Log

## Project
CI Failure Triage Agent — LLM agent that analyzes failed GitHub Actions runs and produces root cause hypotheses.
GitHub repo: https://github.com/Meteordashuaibi/ci-triage-agent

## Completed
- W1: 全部 5 个 practice demo 完成（在 ci-triage-practice repo 里）
  - basic_tool_calling.py
  - structured_output.py
  - retry_exponential_backoff.py
  - token_counting.py
  - error_handling_fallback.py
- W2 进行中:
  - [x] GitHub repo 建好（public）
  - [x] README v1 推上去（架构图 + tech stack，未完成部分用 HTML 注释占位）
  - [ ] 6 阶段 state machine 骨架（空函数 + 类型签名）
  - [ ] GitHub Actions CI 配置

## 当前任务
W2 下一步：实现 6 阶段 state machine 骨架（空函数 + 类型签名 + Pydantic 数据模型）
项目路径：D:\AAAubco\project\ci-triage-agent
Tech stack：Python 3.11, uv, Anthropic SDK, Pydantic, DeepSeek API