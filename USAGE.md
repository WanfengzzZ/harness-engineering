# Harness Engineering Skill 使用指南 v2.0

## 快速开始

### 安装
```bash
cp -r harness-engineering ~/.codebuddy/skills/
```

### 触发场景
- 需要优化代码仓库结构
- 需要建立 AI 可读的文档体系
- 需要配置跨编辑器 Agent 指令文件
- 需要集成 MCP 工具
- Agent 工作效率低，怀疑是环境问题

## 使用示例

### 示例 1：诊断环境
```
使用 harness-engineering skill，诊断当前项目的工程环境成熟度，
找出 Agent 工作效率低的根本原因。
```
**产出**：成熟度评分 + 问题清单 + 改进建议

### 示例 2：新项目设计
```
按照 Harness Engineering v2.0 的三大支柱原则，
为新项目设计完整的工程环境方案。
```
**产出**：AGENTS.md + docs/ 结构 + 架构约束 + CI 配置

### 示例 3：跨编辑器配置
```
帮我配置项目的 Agent 指令文件，团队使用 CodeBuddy、
Cursor 和 Claude Code，需要统一配置。
```
**产出**：AGENTS.md + CLAUDE.md + .cursor/rules/ 配置

### 示例 4：MCP 集成
```
我们项目需要 Agent 能查询数据库和调用内部 API，
帮我设计 MCP 工具集成方案。
```
**产出**：MCP 配置 + 使用约束文档 + AGENTS.md 更新

### 示例 5：实施改进
```
根据 Harness Engineering 原则，帮我实现：
1. 创建 AGENTS.md
2. 编写架构检查脚本
3. 配置 CI 流水线
4. 建立文档验证流程
```
**产出**：可直接使用的文件和脚本

## 核心产出物

### AGENTS.md
- **作用**：Agent 工作地图（~100 行）
- **位置**：项目根目录
- **模板**：`assets/agents-template.md`

### 跨编辑器配置
- **CLAUDE.md**：Claude Code 专属（`assets/claude-md-template.md`）
- **Cursor Rules**：`.cursor/rules/` 格式（`assets/cursor-rules-template.mdc`）
- **指南**：`references/cross-editor-guide.md`

### CI 配置
- **GitHub Actions**：`assets/github-actions-template.yml`
- 包含：lint + test + architecture + docs 验证

### 工具脚本
- `scripts/architecture-lint.py`：架构检查（AST + 循环依赖）
- `scripts/validate-docs.py`：文档验证（断链 + git 集成）
- `scripts/memory-gardening.py`：Agent 记忆清理

## 最佳实践

### 1. 循序渐进
```
P0：AGENTS.md + docs/ + 架构约束
P1：CI 自动化 + 文档验证 + 跨编辑器
P2：可观测性 + MCP + 记忆管理
```

### 2. 持续迭代
- 每周清理代码漂移
- 每月评估健康度
- 每季度更新原则

### 3. 量化跟踪
- 吞吐量：PR 数量/天
- 质量：架构违规次数
- 自主性：Agent 自主完成率
- 健康度：文档新鲜度

## 参考资源

- **检查清单**：`references/checklist.md`
- **黄金原则**：`references/golden-principles.md`
- **跨编辑器指南**：`references/cross-editor-guide.md`
- **MCP 集成指南**：`references/mcp-integration.md`

---

**版本**：2.0.0 | **许可**：MIT
