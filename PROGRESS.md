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
- W3: 进行中
  - [x] 装 PyGithub，连通 GitHub API
  - [x] 探索 workflow runs / jobs / logs 结构
  - [x] 实现 Stage 1 (ingest)：拉 logs + commits，返回 RawRunData
  - [ ] 5 个真实 repo 的 ingest 测试

## 当前任务
W3 下一步：用 5 个真实 repo 测试 ingest，确认不是只针对自己 repo 写死的

项目路径：D:\AAAubco\project\ci-triage-agent
Tech stack：Python 3.11, uv, Anthropic SDK, Pydantic, PyGithub, DeepSeek API
失败 run ID（用于测试）：26022017834