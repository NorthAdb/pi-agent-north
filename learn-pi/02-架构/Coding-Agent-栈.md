# Coding Agent 栈

`packages/coding-agent` 是大多数人说的「Pi」。

## 入口链路

```
src/cli.ts
  → configureHttpDispatcher()
  → src/main.ts 的 main()
       → 创建 services / runtime / session
       → 按 appMode 进入不同 Mode
```

## 三层会话结构

| 层 | 典型文件 | 职责 |
|----|----------|------|
| Services | `core/agent-session-services.ts` | 与 cwd 绑定：设置、鉴权、模型、ResourceLoader |
| Runtime | `core/agent-session-runtime.ts` | 新建 / 恢复 / fork 会话；各模式共用 |
| Session | `core/agent-session.ts` | prompt/steer/followUp、compaction、事件落盘、工具编排 |

注释思想（转述）：**模式只加自己的 I/O；共享逻辑在 AgentSession。**

这就是四种模式能共用一套行为的原因，也是 SDK 能嵌入的原因。

## 默认工具

默认启用：`read`、`bash`、`edit`、`write`（`settings-manager.ts` 的 `DEFAULT_TOOL_NAMES`）。注册表另外还有 `powershell`、`grep`、`find`、`ls`，不在默认集合里。`codemode` 和 `tool_search` 是内置扩展工具，默认不激活。

CLI 可用 `--tools` / `--exclude-tools` / `--no-builtin-tools` 等裁剪。

工具少 = 模型决策空间清晰；复杂能力用 Skill（教模型用外部 CLI）或 Extension（注册新 tool）补。

## 资源发现（ResourceLoader）

启动时发现并装载：

- Extensions（TS，经 jiti 加载）
- Skills
- Prompt templates
- Themes
- Context files（`AGENTS.md` / `CLAUDE.md`）

发现路径通常包括用户目录与项目目录（具体见官方 docs/settings、packages）。  
SDK 可注入自定义 ResourceLoader——这是测试与嵌入的关键缝。

## Extension 运行时

- `ExtensionAPI`：注册工具、命令、快捷键、provider、UI、监听事件等
- `ExtensionContext`：运行时上下文（cwd、model、scopedModels、sessionManager、abort…）
- `ExtensionRunner`：把扩展绑到会话生命周期

扩展与 Pi **同权限**（同进程）。安全靠信任 + 沙箱部署，不靠「扩展商店权限清单」幻想。

## 上下文如何进模型

1. 系统提示（含技能名/描述等渐进披露信息）
2. 项目/全局 context files
3. 会话历史（经 compaction / 分支投影）
4. 当前用户消息（可附带 @file）

细节见官方 `docs/sessions.md`、`compaction.md`、`session-format.md`。

## 配置与换皮钩子

`package.json` 的 `piConfig`：

```json
{
  "piConfig": {
    "name": "pi",
    "configDir": ".pi"
  }
}
```

影响横幅、配置目录、相关环境变量命名。Fork 换皮优先改这里，而不是全局搜字符串。见 [Fork与换皮.md](../05-二次开发/Fork与换皮.md)。

## 调试入口

- 隐藏命令 `/debug` → 写 `~/.pi/agent/pi-debug.log`（TUI 行、最近送给 LLM 的消息）
- 源码运行：`pi-test.ps1` / `pi-test.sh`（保持调用者 cwd）

## 心智图

```
┌─────────────────────────────────────────────┐
│                 Modes (I/O)                 │
│   interactive │ print/json │ rpc │ (sdk)    │
└─────────────────────▲───────────────────────┘
                      │ events / commands
┌─────────────────────┴───────────────────────┐
│              AgentSession                   │
│   tools │ extensions │ compaction │ model   │
└─────────────────────▲───────────────────────┘
                      │
┌─────────────────────┴───────────────────────┐
│           pi-agent-core + pi-ai             │
└─────────────────────────────────────────────┘
```

学编码 Agent 产品层时，优先抓住：**Mode 薄、Session 厚、AI 栈在下。**
