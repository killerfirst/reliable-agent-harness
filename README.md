[English](REAdME.md)  |  [简体中文](README.zh.md)

# Reliable Agent Harness

A minimal agent harness built from scratch for learning and experimenting with reliable agent engineering.


## Goals

This project explores how an agent harness can procide:

- Tool execution boundaries
- Agent loops
- Guardrails
- Verification
- State management
- Context management
- Evaluation
- Sandboxed execution


## Current Status

Currently building V0: a minimal coding agent with a hard-written loop and retricted tools.

## How to use

After filling in the Deepseek key in the env, enter in the terminal: python main.py "task description".

## Model Provider

V0 originally called the OpenAI Responses API. It has been migrated to **DeepSeek**, which is compatible with the `openai` Python SDK but does not provide the Responses API, so the agent loop now uses the Chat Completions API instead.

Configuration in `.env`:

- `DEEPSEEK_API_KEY` — your DeepSeek API key
- `DEEPSEEK_MODEL` — model name, default `deepseek-chat`

Notes:

- `deepseek-chat` fully supports function calling and is the right model for this agent loop; `deepseek-reasoner` has limited tool-calling support and should not be used here.
- The client still comes from the `openai` SDK — only `base_url` points to `https://api.deepseek.com`.
- Tool schemas use the Chat Completions function format (`{"type": "function", "function": {...}}`).
- Harness tool bugs were fixed during this migration: `WORKSPACE` path resolution, an early `return` in `list_files`, and a typo in `replace_text`.

## Roadmap

- [x] V0 - Minimal agent loop
- [ ] V1 - Tool registry and execution limits
- [ ] V2 - Verification and retry
- [ ] V3 - Tracing
- [ ] V4 - State and checkpointing
- [ ] V5 - Context management
- [ ] V6 - Docker sandbox
- [ ] V7 - Evaluation benchmark
