# 学习 Pi Agent（learn-pi）

本目录是面向本仓库（`pi-agent` / fork of [earendil-works/pi](https://github.com/earendil-works/pi)）的**中文学习笔记**，按主题分门别类，帮助你理解：

- Pi 为什么这样设计
- 为什么适合初学者入门「编码 Agent」
- 为什么适合二次开发 / 二次定制
- 设计哲学与刻意省略
- 如何学习、需要什么前置知识

官方英文文档仍是权威来源（`packages/*/docs`、[pi.dev](https://pi.dev)）。本系列是**导读与结构化导图**，并在文中大量指向源码与官方文档路径。

---

## 建议阅读顺序

| 阶段 | 文档 | 目标 |
|------|------|------|
| 0 入门 | [00-概览/什么是-Pi.md](00-概览/什么是-Pi.md) | 一句话定位 + 洋葱分层 |
| 0 入门 | [00-概览/为什么适合学习.md](00-概览/为什么适合学习.md) | 为何对初学者友好 |
| 0 入门 | [00-概览/前置知识.md](00-概览/前置知识.md) | 要先会什么、可以边学边补什么 |
| 1 哲学 | [01-设计哲学/设计哲学.md](01-设计哲学/设计哲学.md) | 核心信条 |
| 1 哲学 | [01-设计哲学/刻意省略.md](01-设计哲学/刻意省略.md) | MCP 为何从省略变成内置扩展 / 无子 Agent / 无权限弹窗… |
| 2 架构 | [02-架构/包地图与依赖.md](02-架构/包地图与依赖.md) | monorepo 分层 |
| 2 架构 | [02-架构/Agent-运行时循环.md](02-架构/Agent-运行时循环.md) | prompt → LLM → tools 循环 |
| 2 架构 | [02-架构/Coding-Agent-栈.md](02-架构/Coding-Agent-栈.md) | CLI / Session / 四种模式 |
| 3 使用 | [03-使用/本地跑起来.md](03-使用/本地跑起来.md) | 从源码安装与运行 |
| 3 使用 | [03-使用/四种运行模式.md](03-使用/四种运行模式.md) | TUI / print / JSON / RPC |
| 3 使用 | [03-使用/会话与上下文.md](03-使用/会话与上下文.md) | session、分支、compaction、AGENTS.md |
| 4 定制 | [04-定制扩展/扩展面总览.md](04-定制扩展/扩展面总览.md) | Extensions / Skills / Packages… |
| 4 定制 | [04-定制扩展/扩展-技能-包.md](04-定制扩展/扩展-技能-包.md) | 各自解决什么问题 |
| 4 定制 | [04-定制扩展/SDK与进程集成.md](04-定制扩展/SDK与进程集成.md) | 嵌入应用与 RPC |
| 5 二次开发 | [05-二次开发/为什么适合二次开发.md](05-二次开发/为什么适合二次开发.md) | 可扩展缝合点 |
| 5 二次开发 | [05-二次开发/如何扩展而不改内核.md](05-二次开发/如何扩展而不改内核.md) | 实操路径 |
| 5 二次开发 | [05-二次开发/Fork与换皮.md](05-二次开发/Fork与换皮.md) | `piConfig`、品牌与配置目录 |
| 6 深读 | [06-深读路径/推荐阅读顺序.md](06-深读路径/推荐阅读顺序.md) | 文档 → 例子 → 源码 |
| 6 深读 | [06-深读路径/关键文件清单.md](06-深读路径/关键文件清单.md) | 先打开哪 20 个文件 |
| 6 深读 | [06-深读路径/Harness北星.md](06-深读路径/Harness北星.md) | AgentHarness 设计方向 |
| 7 参考 | [07-参考/术语表.md](07-参考/术语表.md) | 名词对照 |
| 7 参考 | [07-参考/官方文档地图.md](07-参考/官方文档地图.md) | 指向仓库内官方 docs |

---

## 一句话总结

> **Pi = 极简编码 Agent 线束（harness）**：内核只做「多模型 LLM + Agent 循环 + 会话 + 四个工具 + 终端 UX」，其余工作流靠 **Extensions / Skills / Packages / SDK** 自己拼；**改工作流，不必改内核。**

---

## 与官方文档的关系

| 需求 | 看哪里 |
|------|--------|
| 产品使用 | `packages/coding-agent/docs/` |
| Agent 循环与事件 | `packages/agent/README.md` |
| 多厂商 LLM | `packages/ai/README.md` |
| 终端 UI | `packages/tui/README.md` |
| 贡献与 Agent 规则 | 根目录 `AGENTS.md`、`CONTRIBUTING.md` |
| 本系列（学习导读） | `learn-pi/`（本目录） |

官方 Philosophy（摘录自 `packages/coding-agent/README.md`）：

> Pi is aggressively extensible so it doesn't have to dictate your workflow.
