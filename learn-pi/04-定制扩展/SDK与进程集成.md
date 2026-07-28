# SDK 与进程集成

## SDK：嵌进 Node 应用

入口概念：`createAgentSession()`（及 runtime 相关 API），见：

- `packages/coding-agent/docs/sdk.md`
- `packages/coding-agent/src/core/sdk.ts`
- `packages/coding-agent/examples/sdk/`

你得到的是与 CLI **共享的会话能力**，但 I/O 自己定：

- 自己订阅事件渲染 Web/桌面/日志
- 自己注入 ResourceLoader / 工具 / 模型
- 自己决定是否落盘会话

**何时用 SDK**：你已经有 Node 宿主，想要库式 API。

### 学习阶梯（强制按序）

1. `01-minimal.ts` — 跑通  
2. `05-tools.ts` — 工具  
3. `06-extensions.ts` — 扩展装载  
4. `11-sessions.ts` — 会话  
5. `12-full-control.ts` — 总控  
6. `13-session-runtime.ts` — 替换/恢复会话的 runtime 视角  

## RPC：进程边界集成

- `--mode rpc`
- 文档：`docs/rpc.md`
- 用 JSONL 说话，避免把 coding-agent 打进对方奇异运行时

**何时用 RPC**：宿主不是 Node、或想强隔离进程、或语言绑定更简单。

## JSON 事件流

- `--mode json`
- 文档：`docs/json.md`
- 适合单向消费事件（监控、录制、简单管道）

## Print

- `-p` 文本结果
- 适合「问一句、拿一段」的脚本

## 集成选型

| 需求 | 选择 |
|------|------|
| 同进程、要精细控制 | SDK |
| 跨进程、协议简单 | RPC |
| 只录事件 | JSON |
| Shell 一行出结果 | print |

## 与「适合二次开发」的关系

很多「做自己的 Agent 产品」其实是：

```
自家 UI / 工作流引擎
        │
        ▼
   Pi SDK 或 RPC
        │
        ▼
   同一套工具 + 扩展生态
```

你买到的是 **harness**，不是必须用官方 TUI。TUI 只是第一种 Mode。

## 评测与测试

- `packages/evals`：行为评测方向  
- `packages/coding-agent/test/suite`：faux provider，不烧真实 token  

二次开发自己的扩展时，优先学会在测试里注入 faux / 临时目录，而不是每次手工点 TUI。
