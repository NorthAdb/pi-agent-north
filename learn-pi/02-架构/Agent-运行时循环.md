# Agent 运行时循环

核心在 `packages/agent`。先读 `packages/agent/README.md`，再读 `src/agent-loop.ts`。

## 两层入口

| API | 含义 |
|-----|------|
| `agentLoop` / `runAgentLoop` | 偏纯函数式的循环实现 |
| `Agent` 类 | 有状态封装：持有 messages、订阅事件、`prompt()` |

Coding-agent 的 `AgentSession` 主要建立在这类运行时之上，再叠加会话文件、扩展、工具集。

## 消息两段变换

```
AgentMessage[] ──transformContext()──► AgentMessage[] ──convertToLlm()──► Message[] ──► LLM
```

- **AgentMessage**：应用可扩展（甚至 declaration merging 自定义类型）
- **LLM Message**：只有模型能懂的 `user` / `assistant` / `toolResult`
- **transformContext**：修剪、注入外部上下文（可选）
- **convertToLlm**：过滤 UI-only、转换自定义消息（必需边界）

这是扩展作者最重要的缝：**你在 Agent 世界里加的东西，最终要能投影到 LLM 世界。**

## 无工具时的事件序（简化）

```
prompt("Hello")
├─ agent_start
├─ turn_start
├─ message_start / message_end     (user)
├─ message_start
├─ message_update…                 (assistant 流式)
├─ message_end
├─ turn_end
└─ agent_end
```

## 有工具时的循环

```
user ──► LLM（可能带 tool_calls）
              │
              ▼
     beforeToolCall（可拦截）
              │
              ▼
     执行工具（parallel 默认 / sequential）
              │
              ▼
     afterToolCall
              │
              ▼
     写入 toolResult 消息
              │
              ▼
     下一 turn：LLM 继续
              │
              └─ 直到不再调工具（再处理 follow-up 队列等）
```

关键旋钮：

- 全局 `toolExecution`：`parallel` | `sequential`
- 单工具可强制 `executionMode: "sequential"`
- Steering / Follow-up 队列：运行中插入用户消息的不同时机
- 工具结果可 `terminate`，跳过后续 LLM 调用

## 为什么这样设计

1. **事件足够细**：TUI / RPC / 评测都能挂同一套流  
2. **工具执行与模型调用解耦**：并行工具时完成顺序 ≠ 持久化顺序（文档说明：完成事件按完成序，持久化 toolResult 仍按助手源序）  
3. **钩子可挡工具**：安全扩展不必改循环源码  

## 和 Coding Agent 的关系

```
用户在 TUI 输入
    → AgentSession.prompt / steer / followUp
        → Agent / loop
            → pi-ai stream
            → 内置或扩展 tools
        ← 事件
    → 持久化到 session 文件 + 刷新 UI
```

学循环时，建议实验：

1. SDK `01-minimal.ts`：只看文本流  
2. 带 `bash`/`read` 的会话：对照 README 里「With Tool Calls」图  
3. 打开 `agent-loop.ts`，搜索 `tool` 相关分支  

## 下一步

- 产品如何包这层循环：[Coding-Agent-栈.md](./Coding-Agent-栈.md)
- 持久化北星：[../06-深读路径/Harness北星.md](../06-深读路径/Harness北星.md)
