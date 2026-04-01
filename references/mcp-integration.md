# MCP 工具集成指南

> Model Context Protocol (MCP) 是 2026 年 AI Agent 调用外部工具的统一标准。本指南帮你在 Harness 中集成 MCP 工具。

## 什么是 MCP

MCP 提供了一个标准化协议，让 AI Agent 能够：
- 调用外部工具（数据库查询、API 调用、文件操作）
- 访问外部数据源（实时数据、知识库）
- 执行系统操作（部署、监控、通知）

## 架构

```
Agent ←→ MCP Client ←→ MCP Server ←→ 外部服务
                                      ├── 数据库
                                      ├── API
                                      ├── 文件系统
                                      └── 浏览器
```

## 在 Harness 中集成 MCP

### 1. 在 AGENTS.md 中声明可用工具

```markdown
## 可用 MCP 工具

| 工具 | 用途 | 权限 |
|------|------|------|
| database | 查询数据库 Schema 和数据 | 只读 |
| filesystem | 搜索和读取项目文件 | 读写 |
| browser | UI 自动化测试 | 只读 |
| api-client | 调用内部 API | 按 scope |
```

### 2. 在 docs/ 中记录工具约束

```markdown
# docs/references/mcp-tools.md

## 数据库工具使用规范
- 生产环境只允许 SELECT 查询
- 必须使用参数化查询，禁止字符串拼接
- 查询结果超过 1000 行时必须分页

## API 工具使用规范
- 遵循 API Rate Limit
- 敏感接口需要额外授权
```

### 3. 在 CI 中验证 MCP 配置

```yaml
- name: 验证 MCP 配置
  run: |
    # 检查 MCP 配置文件存在且格式正确
    python scripts/validate-mcp-config.py
```

## 常见 MCP Server

| Server | 用途 | 推荐场景 |
|--------|------|---------|
| `@modelcontextprotocol/server-filesystem` | 文件操作 | 代码导航 |
| `@modelcontextprotocol/server-postgres` | PostgreSQL | 数据查询 |
| `@anthropic/server-browser` | 浏览器自动化 | UI 测试 |
| `whistle-mcp` | 网络代理调试 | API 调试 |

## 安全注意事项

1. **最小权限原则**：MCP 工具只授予必要权限
2. **沙箱执行**：危险操作在沙箱环境中执行
3. **审计日志**：记录所有 MCP 工具调用
4. **配置审查**：MCP 配置变更需要人工审批
5. **生产隔离**：生产环境的 MCP 工具权限严格限制

## 与 Harness 的协同

- **约束层**：在 AGENTS.md 和 docs/ 中声明工具和使用规范
- **反馈层**：MCP 工具的调用结果作为 Agent 的反馈输入
- **验证层**：CI 验证 MCP 配置，审计工具使用合规性
