[English](REAdME.md)  |  [简体中文](README.zh.md)

# Reliable Agent Harness

一个从零开始构建的最小化 Agent Harness，用于学习和实验可靠的 Agent 工程。

## 目标

本项目主要探索 Agent Harness 如何提供以下能力：

- 工具执行边界
- Agent 循环
- 护栏机制
- 验证机制
- 状态管理
- 上下文管理
- 评估
- 沙箱化执行

## 当前状态

目前正在构建 V0：一个带有手写 Agent 循环和受限工具集的最小化 Coding Agent。

## 使用方式

env填入Deepseek key后，终端输入: python main.py "任务描述"

## 模型说明

V0 最初调用 OpenAI 的 Responses API。现已迁移到 **DeepSeek**：DeepSeek 兼容 `openai` Python SDK，但不提供 Responses API，因此 Agent 循环改为使用 Chat Completions API。

`.env` 中的配置：

- `DEEPSEEK_API_KEY` — DeepSeek API 密钥
- `DEEPSEEK_MODEL` — 模型名称，默认 `deepseek-chat`

注意事项：

- `deepseek-chat` 完整支持 function calling，是本 Agent 循环应使用的模型；`deepseek-reasoner` 对工具调用支持有限，不适合本项目。
- 客户端仍使用 `openai` SDK，仅将 `base_url` 指向 `https://api.deepseek.com`。
- 工具 schema 使用 Chat Completions 的 function 格式（`{"type": "function", "function": {...}}`）。
- 本次迁移同时修复了 harness 工具的三处 bug：`WORKSPACE` 路径解析、`list_files` 提前返回、`replace_text` 的拼写错误。

## 路线图

- [x] V0 - 最小化 Agent 循环
- [ ] V1 - 工具注册机制与执行限制
- [ ] V2 - 验证与重试
- [ ] V3 - 运行追踪
- [ ] V4 - 状态与检查点机制
- [ ] V5 - 上下文管理
- [ ] V6 - Docker 沙箱
- [ ] V7 - 评估基准