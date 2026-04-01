# Harness Engineering Skill v2.0

为 Agent 构建高效可工作的工程环境。核心理念：**给 Agent 套上 Harness（马具），让它能独立把活儿干完**。

## v2.0 新特性

- **三大支柱框架**：约束（Constraints）→ 反馈回路（Feedback Loops）→ 验证（Verification）
- **跨编辑器兼容**：AGENTS.md / CLAUDE.md / Cursor Rules / Copilot / Gemini 统一配置
- **MCP 工具集成**：Model Context Protocol 集成指南
- **Agent 记忆管理**：记忆清理和维护脚本
- **多 Agent 协作**：Agent-to-Agent 审核、背景任务编排
- **增强工具脚本**：AST 解析、循环依赖检测、断链检测、git 集成
- **完整 CI 模板**：GitHub Actions 可直接使用

## 安装

```bash
# CodeBuddy
cp -r harness-engineering ~/.codebuddy/skills/

# Cursor
cp -r harness-engineering ~/.cursor/skills/

# 其他编辑器参考对应文档
```

## 使用场景

1. **Agent 效率低** → 诊断工程环境，找出瓶颈
2. **新项目启动** → 从零设计 Harness 方案
3. **跨编辑器配置** → 统一 AGENTS.md / CLAUDE.md / Cursor Rules
4. **MCP 集成** → 让 Agent 调用外部工具
5. **多 Agent 协作** → 设计 Agent 审核和任务编排

## 核心产出

| 产出物 | 说明 |
|--------|------|
| 诊断报告 | 工程环境成熟度评分 + 改进建议 |
| 设计方案 | 文档结构 + 架构约束 + CI 配置 |
| 实施计划 | 分阶段路线图（P0/P1/P2） |
| 实施工具 | Lint 脚本 + CI 模板 + 文档模板 |

## 目录结构

```
harness-engineering-skill/
├── SKILL.md                        # 核心技能定义（三大支柱框架）
├── USAGE.md                        # 使用指南和示例
├── README.md                       # 本文件
├── _meta.json                      # 元数据（v2.0.0）
├── assets/
│   ├── agents-template.md          # AGENTS.md 模板（~80行）
│   ├── claude-md-template.md       # CLAUDE.md 模板
│   ├── cursor-rules-template.mdc   # Cursor Rules 模板
│   └── github-actions-template.yml # CI 配置模板
├── references/
│   ├── checklist.md                # 诊断/实施/维护检查清单
│   ├── golden-principles.md        # 7 条黄金原则
│   ├── cross-editor-guide.md       # 跨编辑器配置指南
│   └── mcp-integration.md          # MCP 工具集成指南
└── scripts/
    ├── architecture-lint.py        # 架构依赖检查（AST + 循环检测）
    ├── validate-docs.py            # 文档验证（断链 + git 集成）
    └── memory-gardening.py         # Agent 记忆清理
```

## 参考

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [AGENTS.md 标准](https://github.com/anthropics/agents-md)

## 案例

**OpenAI 内部实验**：3 人团队，5 个月，100 万行代码，1500 个 PR，0 行人工代码。

---

**版本**：2.0.0 | **许可**：MIT | **作者**：Wanfeng
