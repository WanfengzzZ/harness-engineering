# Release Notes

## v2.0.0 - 2026-04-01

### 🎯 版本主题：三大支柱框架 + 跨编辑器生态

本次大版本升级基于 OpenAI Harness Engineering 最新实践、Martin Fowler 的分类框架、以及 2026 年 Agent 工程环境最佳实践，对 Skill 进行了全面重构。

---

### 🏗️ 架构重构

**五原则 → 三大支柱框架**

v1.0 的五大原则重组为更清晰的三大支柱：

| 支柱 | 内容 | 对应 v1.0 原则 |
|------|------|---------------|
| **约束（Constraints）** | 仓库即记录、架构约束、品味不变式、跨编辑器配置 | 原则 1 + 3 |
| **反馈回路（Feedback Loops）** | Agent 可读性、应用可观测性、CI/CD、文档园艺、记忆管理 | 原则 2 + 4 |
| **验证（Verification）** | 自动化测试、Agent-to-Agent 审核、吞吐量合并、质量度量 | 原则 5 |

---

### 🆕 新增功能

#### 1. 跨编辑器配置体系
- 新增 `references/cross-editor-guide.md` - 统一配置指南
- 新增 `assets/claude-md-template.md` - Claude Code 配置模板
- 新增 `assets/cursor-rules-template.mdc` - Cursor Rules 配置模板
- 覆盖 6 种工具：AGENTS.md / CLAUDE.md / Cursor Rules / Copilot / Gemini / CodeBuddy

#### 2. MCP 工具集成
- 新增 `references/mcp-integration.md` - Model Context Protocol 集成指南
- 包含架构设计、安全规范、与 Harness 协同策略

#### 3. Agent 记忆管理
- 新增 `scripts/memory-gardening.py` - 记忆清理维护脚本
- 支持过时检测、重复检测、价值评估
- 自动化记忆归档和迁移建议

#### 4. 多 Agent 协作模式
- 新增串行/并行/审核/背景任务四种协作模式
- Agent-to-Agent 审核流程设计
- 背景任务编排方案

#### 5. 完整 CI 配置
- 新增 `assets/github-actions-template.yml` - 可直接使用的 CI 模板
- 包含：lint + test + architecture + docs 验证

---

### 🔧 增强改进

#### architecture-lint.py v2.0
- ✅ Python 文件使用 AST 精确解析 import（替代正则）
- ✅ TS/JS 文件增强正则（支持 dynamic import、re-export）
- ✅ 新增**循环依赖检测**（层间）
- ✅ 扩展层映射规则（新增 models/schemas/usecases/views/screens 等）
- ✅ 扩展横切关注点白名单（新增 common/lib/helpers）
- ✅ 违规报告包含**修复指导**
- ✅ 支持 `@/` 路径别名

#### validate-docs.py v2.0
- ✅ 新增**断链检测**（检查 markdown 中引用不存在的文件）
- ✅ 新增 **git 集成**（使用 git log 精确计算文档修改时间）
- ✅ 新增**文件结构完整性检查**（AGENTS.md、docs/ 等必需文件）
- ✅ 支持检查推荐文件（ARCHITECTURE.md、design-docs/ 等）

#### golden-principles.md v2.0
- 从 10 条精简为 **7 条核心原则**
- 每条原则增加**代码示例**（❌ 错误 vs ✅ 正确）
- 增加具体的**实施建议**

#### checklist.md v2.0
- 新增**跨编辑器配置**检查项
- 新增 **MCP 工具集成**检查项
- 新增 **Agent 记忆管理**检查项
- 增加**度量指标**表格

#### agents-template.md
- 从 283 行精简到 **72 行**（符合 ~100 行地图原则）
- 更聚焦于 Agent 工作所需的核心信息

---

### 📊 数据对比

| 维度 | v1.0 | v2.0 | 变化 |
|------|------|------|------|
| 架构框架 | 五原则散列 | 三大支柱 | 重构 |
| 编辑器支持 | 2 种 | 6 种 | +4 |
| 工具脚本 | 2 个 | 3 个 | +1 |
| 模板文件 | 1 个 | 4 个 | +3 |
| 参考文档 | 2 个 | 4 个 | +2 |
| 黄金原则 | 10 条 | 7 条 | 精简 |
| AGENTS.md 模板 | 283 行 | 72 行 | -74% |
| architecture-lint | 正则解析 | AST + 循环检测 | 增强 |
| validate-docs | 仅检查年龄 | 断链 + git + 结构 | 增强 |

---

### ⚠️ 破坏性变更

1. `SKILL.md` 完全重写，从五原则结构改为三大支柱框架
2. `golden-principles.md` 从 10 条精简为 7 条
3. `agents-template.md` 大幅精简，旧模板内容需手动迁移
4. `_meta.json` 中 `author` 字段从 "OpenAI Community" 改为 "Wanfeng"

---

### 🙏 致谢

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/) - 核心理念来源
- [Martin Fowler: Exploring Gen AI - Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) - 三大支柱分类框架
- [AGENTS.md 社区标准](https://github.com/anthropics/agents-md) - 跨编辑器配置标准

---

## v1.0.0 - 2026-03-30

初始发布版本。

### 核心内容
- 五大核心原则（代码仓库即记录、Agent 可读性、规范架构、应用可读性、吞吐量合并）
- AGENTS.md 模板
- 10 条黄金原则
- 架构依赖检查脚本
- 文档验证脚本
- 诊断/实施/维护检查清单
