# Fork 与换皮

## 官方支持的换皮

`packages/coding-agent/docs/development.md`：

```json
{
  "piConfig": {
    "name": "pi",
    "configDir": ".pi"
  }
}
```

同时调整 `bin` 等字段。影响：

- CLI 横幅 / 产品名  
- 配置目录名  
- 相关环境变量命名习惯  

**优先改配置，而不是全局替换字符串。**

## 路径解析注意

三种运行方式：npm 全局、独立 binary、tsx 源码。  
包内资源路径应走 `src/config.ts` 的 `getPackageDir` / `getThemeDir`，不要对 `__dirname` 写死假设。

## Fork 策略建议

### 轻度 fork（推荐）

- 保留与上游同步能力  
- 自有品牌用 `piConfig`  
- 差异放在私有 packages（extensions/skills）仓库  
- 内核仅 cherry-pick 或定期 merge  

### 重度 fork（谨慎）

- 改 agent 循环、会话格式、扩展 API  
- 成本：难以跟上游；要自己维护模型目录生成、发布管道  

若目标是产品差异化，**重度 fork 通常输给「薄宿主 + 官方 coding-agent + 私有扩展」**。

## 本仓库（North fork）场景

你已有 `pi-agent-north` 这类 fork 时：

1. 明确 fork 目的：跟上游学习？做内部分发？改协议？  
2. 若是学习/内部分发：保持 remote 可拉取 upstream，差异放扩展  
3. 贡献回上游时遵循 `CONTRIBUTING.md`（新贡献者 issue/PR 默认自动关闭等策略）  

## 上游地址

- 典型上游：`https://github.com/earendil-works/pi`  
- 文档与 npm 作用域：`@earendil-works/*`  
- 网站：https://pi.dev  

添加 upstream remote 示例：

```powershell
cd E:\AI-Tech\pi-agent
git remote add upstream https://github.com/earendil-works/pi.git
git fetch upstream
```

## 发布自己的发行版？

若要公开发布改名后的 CLI：

- 处理 npm 包名、二进制名、文档商标  
- 遵守 MIT 与依赖许可证  
- 认真对待 supply-chain（继承上游的 ignore-scripts / 钉版本文化）  
- 模型数据生成与 release source archive 流程见根 README  

对大多数二次开发：**不需要发布内核**；发布你的 `pi package` 即可。
