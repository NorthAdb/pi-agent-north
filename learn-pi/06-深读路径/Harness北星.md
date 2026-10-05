# 两条 Harness，不要混成一条

1.0.0 删掉了 `packages/agent` 里的 `AgentHarness`、会话仓库和压缩库。`packages/agent/docs/` 也不在了。现在要先分清你打开的是哪条路径。

| 路径 | 你实际跑到的代码 | 什么时候读 |
|------|------------------|------------|
| 日常 `pi` | `Agent` + `AgentSession` + JSONL `SessionManager` | 使用、扩展、读 coding-agent |
| 实验持久化 | `@earendil-works/pi-durable` 的 `Harness` | 要做崩溃可恢复、提交先于展示的运行时 |

两条都叫 harness，解决的问题不一样。低层循环只负责「这一轮怎么叫模型和工具」。产品还要决定历史放哪、压缩切在哪、扩展什么时候加载。

## 日常路径：会话文件是产品的真相

`packages/coding-agent/src/core/session-manager.ts` 把一次会话写成 append-only JSONL。条目不止消息，还有模型切换、压缩、分支摘要。当前叶子是 `leafId`，从叶子走到根才是模型这一轮该看见的历史。

压缩在 `packages/coding-agent/src/core/compaction/compaction.ts`，不在 agent 包里。它替换的是送给模型的投影，不删 JSONL 原文。

扩展、技能、工具、信任门禁都在 coding-agent。`packages/agent` 只提供循环和事件。

## 实验路径：pi-durable

`packages/durable/README.md` 开头就写了：**Experimental. The API changes without notice.**

它解决的是另一件事：对话、模型回合、工具调用先提交到存储，进程死在半路，重新打开还能从上次的检查点继续。存储可以是内存、JSONL 或 SQLite（`src/storage/sqlite/node.ts`）。1.0 之前单独的 `packages/session-backends` 没有了，SQLite 收进这个包。

概念上它和日常 CLI 不是同一套对象：

- **Harness**：一份打开的存储，加上在上面跑 agent 的机器
- **Conversation**：不可变条目组成的转录
- **Commit**：一次原子写入。条目、文档、任务要么一起落下，要么都不落
- **Task**：每一步存检查点。生成模型回复的是内置任务 `pi.generation`，它再拥有工具任务

规范在 `packages/durable/docs/spec.md`（Pico5）。coding-agent 里引用它的代码在 `src/experimental/`，不是 `pi` 默认打开会话的那条路。`packages/coding-agent/package.json` 的 dependencies 里没有 `pi-durable`。

## 学习者怎么用

1. 先把 `packages/agent/src/agent-loop.ts` 的双层 while、`prepareRequest`、`finishTurn` 读懂。
2. 再读 `session-manager.ts` 和 `compaction.ts`，这是你用 `pi` 时真正落盘的模型。
3. 只有要做「死了还能接着跑」的宿主时，再打开 `packages/durable/README.md`。不要把 spec 里的相位和对象名套回今天的 `AgentSession`。

## 相关路径

- `packages/agent/README.md` — 循环、事件、`prepareRequest` / `finishTurn`
- `packages/coding-agent/src/core/session-manager.ts`
- `packages/coding-agent/src/core/compaction/compaction.ts`
- `packages/durable/README.md`
- `packages/durable/docs/spec.md`
- `packages/coding-agent/src/experimental/durable/`
