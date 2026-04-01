# 跨编辑器 Agent 配置指南

> 2026 年，AGENTS.md 已成为事实标准（60,000+ repos 采用）。不同 AI 编辑器有各自的专属配置文件，本指南帮你统一管理。

## 配置文件总览

| 文件 | 工具 | 位置 | 加载方式 |
|------|------|------|---------|
| `AGENTS.md` | 通用（所有工具） | 项目根目录 | 自动加载 |
| `CLAUDE.md` | Claude Code | 项目根目录 | 自动加载 |
| `.cursor/rules/*.mdc` | Cursor | `.cursor/rules/` | 按 globs 匹配 |
| `.github/copilot-instructions.md` | GitHub Copilot | `.github/` | 自动加载 |
| `GEMINI.md` | Gemini CLI | 项目根目录 | 自动加载 |
| `.codebuddy/rules/*.md` | CodeBuddy | `.codebuddy/rules/` | 按规则匹配 |

## 分层策略

```
┌─────────────────────────────────────┐
│     AGENTS.md（通用基座）           │ ← 所有工具都读取
│     项目概述 + 架构规则 + 文档导航   │
├─────────────────────────────────────┤
│     工具专属配置（增强层）           │ ← 各工具独有功能
│  CLAUDE.md / .cursor/rules/ / ...   │
└─────────────────────────────────────┘
```

**核心原则**：
- AGENTS.md 放**通用信息**：项目概述、架构规则、文档导航、质量标准
- 工具专属文件放**增强配置**：工具特有指令、格式偏好、特殊规则

## AGENTS.md 编写要点

1. **控制在 ~100 行**：是地图，不是百科全书
2. **包含文档导航**：指向 docs/ 下的详细文档
3. **明确架构约束**：分层规则、依赖方向
4. **列出常用命令**：lint、test、build、deploy
5. **定义质量标准**：PR 检查项、测试要求

模板见 `assets/agents-template.md`

## CLAUDE.md 编写要点

Claude Code 特有功能：
- 支持 `~/.claude/CLAUDE.md` 全局配置
- 支持子目录 `CLAUDE.md` 覆盖
- 支持 `CLAUDE.local.md`（不提交到 Git）

建议内容：
- 项目概述（技术栈、架构）
- Claude 特有的代码风格偏好
- 常用命令和工作流程
- 禁止事项清单

模板见 `assets/claude-md-template.md`

## Cursor Rules 编写要点

Cursor 新格式（`.cursor/rules/*.mdc`）支持：
- `description`：规则描述（Agent 用于判断是否应用）
- `globs`：文件匹配模式
- `alwaysApply`：是否总是应用

建议拆分为多个 .mdc 文件：
```
.cursor/rules/
├── architecture.mdc    # 架构约束（alwaysApply: true）
├── frontend.mdc        # 前端规则（globs: "src/ui/**"）
├── backend.mdc         # 后端规则（globs: "src/service/**"）
└── testing.mdc         # 测试规则（globs: "**/*.test.*"）
```

模板见 `assets/cursor-rules-template.mdc`

## GitHub Copilot 配置

`.github/copilot-instructions.md`：
- 项目约定和编码标准
- 注意：内容会作为系统指令注入，保持简洁

## 维护建议

1. **AGENTS.md 优先维护**：它是所有工具的公约数
2. **工具专属文件按需添加**：团队用什么工具就配什么
3. **保持一致性**：各文件的架构规则不应矛盾
4. **定期审查**：每月检查配置是否与项目实际一致
5. **不要重复**：通用信息只放 AGENTS.md，专属文件只放增强内容
