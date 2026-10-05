# 什么是 Pi

## 定位

Pi（本仓库的产品入口是 `@earendil-works/pi-coding-agent`，CLI 名通常为 `pi`）是一个**极简的终端编码 Agent 线束（coding agent harness）**。

它不是「功能最全的 IDE 插件」，也不是「把所有 Agent 概念都内置进去」的产品。它刻意保持：

- **核心小**：默认启用四个工具（`read` / `bash` / `edit` / `write`）。注册表里还有 `powershell` / `grep` / `find` / `ls`，但不在默认集合里。再加上会话、模型、终端 UI
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
| `pi-agent-core` | 循环与事件。1.0 起不含会话、压缩、Harness |
| `pi-tui` | 终端 UI（差分渲染） |
| `pi-coding-agent` | 面向开发者的编码 Agent CLI / SDK。日常 JSONL 会话在这里 |
| `pi-durable` | 实验性可恢复 Harness。SQLite / JSONL 存储在包内。日常 `pi` 不走它 |
| `pi-codemode` | QuickJS 沙箱里跑 JS，能力是调用被注入的工具 |
| `pi-mcp` | 独立 MCP 客户端（stdio / Streamable HTTP / OAuth） |
| `pi-server` | 实验性服务封装 |

各包 1.0.2 lockstep 同版本；完整依赖图与构建顺序见 [包地图与依赖.md](../02-架构/包地图与依赖.md)。

你当前工作区是这个 fork。内容对应上游 1.0.2。

## 「Harness」是什么意思

在 Agent 语境里，**harness（线束 / 驾驭层）** 指：把模型、工具、会话持久化、事件、扩展点**绑在一起**，让应用能安全地跑多轮「想 → 调工具 → 再想」的循环。

Pi 把这件事拆成三条不要混用的路径：

1. **低层 `Agent` / `agentLoop`**：内存态循环 + 事件流。`packages/agent` 现在只有这一层。
2. **产品会话**：`AgentSession` + JSONL 树。这是 `pi` 每天在用的 harness。
3. **实验 `Harness`（pi-durable）**：先提交再展示，崩溃后可恢复。不是 CLI 的默认会话。

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
agent-core（只有循环、工具执行、事件）
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

子 Agent、权限弹窗、Plan Mode、内置 TODO、后台 bash……详见 [刻意省略.md](../01-设计哲学/刻意省略.md)。

这些不是「做不出来」，而是**不该钉死在内核里**——用扩展或包按你的安全与流程重做。

MCP 是这条原则的边界样本：0.99.0 起它以内置扩展形式随 Pi 发布，1.0.2 仍如此。默认启用的工具没有增加 MCP。默认 `exposure: "codemode"`，工具不声明给模型，脚本用 `searchTools()` 按需发现。非 `direct` 的服务器不挡住第一条 prompt。

## 相关链接

- 产品站：[pi.dev](https://pi.dev)
- 官方文档索引：`packages/coding-agent/docs/index.md`
- 设计哲学长文（作者博客，README 引用）：[pi coding agent](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)
- MCP 上下文预算的经典论证：[What if you don't need MCP?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)——0.99 的内置 MCP + codemode 正是这条批评的工程回答
