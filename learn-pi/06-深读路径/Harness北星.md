# Harness 北星（AgentHarness）

## 先分清「今天的代码」和「文档中的北星」

| 层面 | 现状（简化） |
|------|----------------|
| Coding-agent 日常路径 | 大量使用 `Agent` + `AgentSession` + JSONL 会话文件 |
| `packages/agent/docs/harness.md` 等 | 描述 **AgentHarness** 的持久化、相位、钩子、可重入等目标设计 |

学习时不要把设计文档的每一句都当成「当前每一行代码已完全如此」。  
把它当作：**官方认为正确的长期架构方向**。二次开发深水区以此为指南针。

## Harness 要解决什么

低层 loop 已经能跑工具循环；产品还需要：

- 会话持久化与恢复  
- 资源（skills/templates）与系统提示解析  
- 运行中改配置 vs 当前 turn 快照不互相踩脚  
- 忙碌相位（turn / compaction / retry）下哪些 API 可调用  
- 钩子失败、pending writes、save points 的确定性  

`AgentHarness` 文档把这些收成显式模型。

## 四类状态（文档概念）

摘自 / 转述 `agent-harness.md`：

1. **Harness config**（最新配置）：model、tools、resources、system prompt…  
   - getter 返回最新配置  
   - setter 立即更新，但**影响下一 turn**，不改写飞行中的 provider 请求  

2. **Turn snapshot**：一次 LLM turn 冻结的输入视图（消息、工具、prompt、stream options…）  

3. **Session**：已持久化条目；读不包括尚未 flush 的队列  

4. **Pending session writes**：忙碌时排队的写入，在 save point / 结束时确定性落盘  

## 相位

```ts
type AgentHarnessPhase = "idle" | "turn" | "compaction" | "branch_summary" | "retry";
```

结构操作（如 `prompt`、`compact`、树导航）要求 idle；turn 中允许 steer/followUp/abort 等。  
忙碌时再 `prompt` → `busy` 错误。这是并发心智的核心。

## 事件 vs 钩子 vs 可观测性

- **Events**：已提交状态的观察  
- **Hooks**：参与语义（可 block tool、变换上下文）  
- **OpenTelemetry 等**：旁路遥测，不与 hooks 混用职责  

详见 `packages/agent/docs/hooks.md`、`observability.md`。

## Durable / 半持久

`durable-harness.md` 方向：会话可恢复，但 **工具与扩展由宿主在恢复时重新提供**（不把整个 JS 世界序列化）。  

这对二次开发的含义：

- 你可以升级工具实现再打开旧会话  
- 宿主必须在 resume 时装配好等价能力，否则行为会漂  

## 学习者怎么用这些文档

1. 先精通当前 `Agent` 事件循环  
2. 再读 harness 文档的「状态分类」与「相位」两节  
3. 在 coding-agent 里对照：哪些像 snapshot，哪些像 live config  
4. 做扩展时避免在 hook 里乱调可能死锁的 settlement API（文档有警告）  

## 相关路径

- `packages/agent/docs/agent-harness.md`  
- `packages/agent/docs/harness.md`  
- `packages/agent/docs/durable-harness.md`  
- `packages/agent/docs/hooks.md`  
- `packages/agent/src/harness/`（实现演进中）
