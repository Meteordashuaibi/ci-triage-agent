# Progress Log

## Project
CI Failure Triage Agent — LLM agent that analyzes failed GitHub Actions runs and produces root cause hypotheses.
GitHub repo: https://github.com/Meteordashuaibi/ci-triage-agent

## Completed
- W1: 全部 5 个 practice demo 完成
- W2: 全部完成 ✅
  - [x] GitHub repo + README v1
  - [x] 6 阶段 state machine 骨架 + Pydantic 数据模型
  - [x] pyproject.toml + uv + GitHub Actions CI（绿勾）
- W3: 全部完成 ✅
  - [x] 装 PyGithub，连通 GitHub API
  - [x] 探索 workflow runs / jobs / logs 结构
  - [x] 实现 Stage 1 (ingest)：拉 logs + commits，返回 RawRunData
  - [x] 5 个真实 repo 的 ingest 测试全部通过

## 当前任务
W4 (5/22–5/31): Stage 2 — Parse
- 从 pytest 输出里提取失败文件、行号、失败类型
- 支持 4 种失败类型：assertion / import / collection / exception
- 写解析准确率测试 30 个样本
