# 什么是 Pi

## 定位

Pi（本仓库的产品入口是 `@earendil-works/pi-coding-agent`，CLI 名通常为 `pi`）是一个**极简的终端编码 Agent 线束（coding agent harness）**。

它不是「功能最全的 IDE 插件」，也不是「把所有 Agent 概念都内置进去」的产品。它刻意保持：

- **核心小**：默认四个工具（`read` / `write` / `edit` / `bash`），加上会话、模型、终端 UI
- **缝合点多**：用 TypeScript Extensions、Skills、Prompt Templates、Themes、Pi Packages、SDK / RPC 扩展
- **可嵌入**：同一套 Session 可跑在交互 TUI、打印模式、JSON 事件流、RPC、或你自己的 Node 应用里

官方一句话（`packages/coding-agent/README.md`）：

> Adapt pi to your workflows, not the other way around, without having to fork and modify pi internals.

翻译：**让 Pi 适应你的工作流，而不是反过来；不必 fork 改内核。**

## 本仓库是什么

根 README 称整个 monorepo 为 **Pi Agent Harness**：

| 包 | 角色 |
|----|------|
| `pi-ai` | 统一多厂商 LLM API |
| `pi-agent-core` | Agent 运行时（工具调用、状态、事件） |
| `pi-tui` | 终端 UI（差分渲染） |
| `pi-coding-agent` | 面向开发者的编码 Agent CLI / SDK |
| `pi-storage-sqlite-node` | 可选 SQLite 会话后端 |
| `pi-server` | 实验性服务封装 |

你当前工作区 `E:\AI-Tech\pi-agent` 是 fork（如 NorthAdb/pi-agent-north），学习内容与上游一致。

## 「Harness」是什么意思

在 Agent 语境里，**harness（线束 / 驾驭层）** 指：把模型、工具、会话持久化、事件、扩展点**绑在一起**，让应用能安全地跑多轮「想 → 调工具 → 再想」的循环。

Pi 把这件事拆成两层常见抽象：

1. **低层 `Agent` / `agentLoop`**：内存态循环 + 事件流（今天 coding-agent 仍大量使用）
2. **高层 `AgentHarness`**：文档中的「持久化与生命周期」北星设计（会话日志为真相，工具/扩展由宿主在恢复时再注入）

详见 [Harness北星.md](../06-深读路径/Harness北星.md)。

## 洋葱分层（心智模型）

从外到内理解最省力：

```
你（用户 / 宿主应用）
    │
    ▼
coding-agent（产品：CLI、会话、扩展、Skills、四种模式）
    │
    ├─► tui（终端渲染，与 AI 栈无关）
    │
    ▼
agent-core（循环、工具、事件、Session/Harness）
    │
    ▼
pi-ai（多厂商 stream / tools / 模型目录）
    │
    ▼
各 LLM Provider API
```

**初学者**：先当「会说话的终端程序员」用（coding-agent）。  
**二次开发者**：从外层扩展面下手；只有要改协议/循环语义时才沉到 agent / ai。

## Pi 默认给你什么

- 交互终端编程助手
- 订阅或 API Key 多模型切换
- 会话文件（可继续、可分支、可 compaction）
- 项目上下文文件（`AGENTS.md` / `CLAUDE.md`）
- 扩展生态：自己写或 `pi install` 第三方包

## Pi 默认不给你什么（刻意）

MCP、子 Agent、权限弹窗、Plan Mode、内置 TODO、后台 bash……详见 [刻意省略.md](../01-设计哲学/刻意省略.md)。

这些不是「做不出来」，而是**不该钉死在内核里**——用扩展或包按你的安全与流程重做。

## 相关链接

- 产品站：[pi.dev](https://pi.dev)
- 官方文档索引：`packages/coding-agent/docs/index.md`
- 设计哲学长文（作者博客，README 引用）：[pi coding agent](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)
- MCP 立场：[What if you don't need MCP?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)
