# NOTES（教学偏好与工作笔记）

## 用户偏好（来自首次需求说明）

- 语言：中文教学。
- 起点假设：不要当成已理解 Agent Harness 的人。第一个问题必须是"为什么 LLM 自己不能成为 Agent"。
- 每个新概念必须回答 7 问：解决什么问题 / 没有它会怎样 / 输入 / 输出 / 谁控制 / 和前一个概念的关系 / Pi 源码哪里实现。
- 每张 Archify 图之后按固定三段讲：①这张图要解决什么问题 ②如何从图上读懂 Pi ③这张图在整个学习体系中的位置。
- 不大量粘贴源码；建立「概念 → 模块 → 调用链 → 数据流」映射，伪代码 10–30 行以内。
- 明确区分三层证据：源码事实 / 官方文档 / 架构推断。
- 课程为 14 阶段固定主线（用户已给出完整大纲，见 lessons/COURSE 总纲）。
- 最终交付物：Minimal Pi-like Agent Harness 手写练习（需求→接口→数据结构→运行流程→最小实现→测试→扩展）。

## 工作笔记

- 仓库结构（已核实，0.99.1）：packages/{chord, telemetry, tui, ai, durable, agent, protocol, client, server, codemode, mcp, session-backends, coding-agent, evals}。
- 2026-09 同步上游 0.99.1（merge `9d7c377e`）：新增 `codemode` / `mcp` 两个包，MCP 成为可替换的内置扩展。
  第 15 课据此重写；Diagram 14 的 spec 与渲染 HTML 文案同步更新，并用 headless Chrome 重拍了 4 张视口截图
  （Archify 不在本机，渲染件是文本级替换，下次可用 Archify 重新渲染覆盖）。
- fork 内已有 learn-pi/ 中文概览导读（22 篇），本课程不与其重复：learn-pi 是"是什么/怎么用"，本课程是"为什么这样设计 + 源码逆向"。
- Archify 图表嵌入 lessons/*.html；每个 lesson 一个主题一个图。
- 证据标注约定：【源码】【文档】【推断】。
