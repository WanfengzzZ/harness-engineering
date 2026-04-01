---
name: harness-engineering-skill
description: 为 Agent 构建高效可工作的工程环境。当需要优化代码仓库结构、文档组织、反馈回路、自动化流程，使 Agent 能够自主高效地完成开发任务时使用此技能。核心目标：让代码、文档、测试对 AI 可读而非仅对人可读。
---

# Harness Engineering v2.0

**Harness Engineering** 是 2026 年最重要的 AI 工程范式。核心理念：**给 Agent 套上 Harness（马具）——不是告诉它做什么，而是搭建让它能独立把活儿干完的整套工程环境**。

## 核心认知

### 三阶段演进

1. **2024 提示词工程**：教模型听懂话，优化单次对话输入
2. **2025 上下文工程**：让模型看到全貌，构建完整信息环境
3. **2026 Harness Engineering**：给 Agent 搭整套能自己干活的工作环境

**本质区别**：
- 提示词工程 = 告诉它做什么
- 上下文工程 = 让它看到全貌
- Harness Engineering = 让它有工具、有规则、有反馈，能独立把活儿干完

### 核心问题

> **你是否给 AI 提供了一个它可以自我迭代的环境？**

自问清单：
- [ ] 架构约束是写在文档里，还是只存在于口头约定？
- [ ] 测试能被自动运行，还是需要人手动触发？
- [ ] 设计决策有记录，还是散落在聊天记录里？
- [ ] 代码仓库对 AI 可读吗？（不仅是人可读）
- [ ] Agent 出错后能自己发现并修复吗？

## 触发场景

**使用此技能**：
- 需要优化代码仓库结构，使 Agent 能够自主导航和工作
- 需要建立对 AI 可读的文档体系（而非仅对人可读）
- 需要设计自动化反馈回路（CI/CD、自动测试、代码检查）
- 需要配置跨编辑器的 Agent 指令文件（AGENTS.md / CLAUDE.md / Cursor Rules）
- 需要集成 MCP 工具让 Agent 调用外部服务
- 需要设计多 Agent 协作和审核流程
- 需要管理 Agent 的工作记忆和跨会话上下文
- 遇到 Agent 工作效率低，怀疑是环境问题而非模型问题

**不适用**：
- 单纯的代码实现任务
- 单纯的需求分析
- 单纯的提示词优化
- 与 Agent 工程环境无关的任务

---

## 三大支柱框架

Harness Engineering 的核心由三大支柱构成（参考 Martin Fowler 分类框架）：

```
┌─────────────────────────────────────────────────┐
│              Harness Engineering                │
├─────────────┬──────────────┬────────────────────┤
│  约束        │  反馈回路     │  验证              │
│ Constraints  │ Feedback     │ Verification       │
│              │ Loops        │                    │
├─────────────┼──────────────┼────────────────────┤
│ 仓库即记录   │ Agent 可读性  │ 自动化测试         │
│ 架构约束     │ 应用可观测性  │ Agent-to-Agent 审核│
│ 品味不变式   │ CI/CD 自动化  │ 吞吐量合并理念     │
│ 跨编辑器配置 │ 文档园艺      │ 质量度量           │
│              │ Agent 记忆    │                    │
└─────────────┴──────────────┴────────────────────┘
```

### 支柱一：约束（Constraints）

> 通过强制执行不变量来引导 Agent，而非微观管理

#### 1.1 代码仓库即记录系统

**核心**：Agent 看不到的信息 = 不存在

**做法**：
- 所有知识版本化存储在代码仓库内（`docs/` 目录）
- AGENTS.md 作为地图（~100 行），指向结构化文档
- 设计决策、产品原则、工程规范全部内化到仓库
- 禁止知识外置到 Notion、飞书、Google Docs

**文档结构**：
```
docs/
├── design-docs/           # 设计文档
│   ├── index.md          # 索引
│   └── core-beliefs.md   # 核心理念
├── exec-plans/           # 执行计划
│   ├── active/           # 活跃计划
│   └── tech-debt-tracker.md
├── product-specs/        # 产品规格
├── references/           # 参考文档
└── generated/            # 自动生成（DB Schema 等）
```

#### 1.2 架构约束代码化

**核心**：约束不能只存在于文档，必须被工具强制执行

**分层架构**：
```
Types → Config → Repo → Service → Runtime → UI
         ↓          ↓         ↓         ↓
      Providers（横切关注点）
```

**实现方式**：
- 自定义 Lint 脚本验证依赖方向（见 `scripts/architecture-lint.py`）
- CI 阻塞违规提交
- 错误信息必须包含修复指导
- 定期扫描架构漂移

#### 1.3 品味不变式

将团队的隐性规则显性化编码：
1. 禁止 YOLO 式探测数据，必须验证边界
2. 优先使用共享 utility 包，而非手工辅助工具
3. 所有日志必须结构化，包含 trace_id
4. 错误处理必须一致，包含修复指导
5. 配置外部化，禁止硬编码
6. 命名遵循统一约定

详见 `references/golden-principles.md`

#### 1.4 跨编辑器配置

2026 年 AGENTS.md 已成为事实标准（60,000+ repos 采用），但不同 AI 编辑器有专属配置：

| 文件 | 工具 | 作用 |
|------|------|------|
| `AGENTS.md` | 通用（所有工具） | Agent 工作地图，~100 行 |
| `CLAUDE.md` | Claude Code | Claude 专属指令和偏好 |
| `.cursor/rules/*.mdc` | Cursor | 支持 globs/alwaysApply 的规则 |
| `.github/copilot-instructions.md` | GitHub Copilot | Copilot 项目指令 |
| `GEMINI.md` | Gemini CLI | Gemini 专属配置 |

**策略**：AGENTS.md 作为通用基座，工具专属文件作为增强层。
详见 `references/cross-editor-guide.md`，模板见 `assets/` 目录。

### 支柱二：反馈回路（Feedback Loops）

> 让 Agent 能感知自己的工作效果，形成自我纠正能力

#### 2.1 为 Agent 可读性优化

**关键认知**：Agent 运行时无法访问的上下文 = 不存在

**优化策略**：
- **渐进式披露**：AGENTS.md（100 行地图）→ 指向 → docs/ 目录（结构化知识）
- **架构约束代码化**：写进 Lint 工具，而非只存在文档
- **文档可验证**：CI 自动检查文档是否与代码同步

#### 2.2 应用可观测性

让 Agent 能直接读取 UI、日志、指标，自主 QA：

**UI 可读性**：
- 使应用可根据 git worktree 启动
- 接入 Chrome DevTools 协议到 Agent 运行时
- 支持 DOM 快照和屏幕截图

**日志/指标可读性**：
- 结构化日志（LogQL 查询）
- 性能指标（PromQL 查询）
- trace_id / span_id 追踪

#### 2.3 CI/CD 自动化验证

完整的 CI 流水线应包含：
```yaml
必需检查:
  - lint: 代码质量检查
  - architecture: 架构依赖检查
  - test: 单元测试 + 集成测试
  - docs: 文档同步检查
  - typecheck: 类型检查
```
完整 CI 模板见 `assets/github-actions-template.yml`

#### 2.4 文档园艺（Doc Gardening）

定期运行后台 Agent 清理"文档残渣"：
- 扫描过时文档（> 90 天未更新）
- 检测断链（引用不存在的文件）
- 自动发起修复 PR
- 使用 `scripts/validate-docs.py` 执行

#### 2.5 Agent 记忆管理

Agent 需要跨会话保持上下文：

**记忆类型**：
- **工作记忆**：当前任务的上下文（自动管理）
- **项目记忆**：设计决策、架构约定（存储在 `.codebuddy/memory/` 或 `docs/`）
- **经验记忆**：踩过的坑、成功的模式（定期归档）

**记忆维护**：
- 定期清理过时记忆
- 合并重复记忆
- 将高价值经验迁移到 docs/
- 使用 `scripts/memory-gardening.py` 自动化维护

### 支柱三：验证（Verification）

> 确保 Agent 产出的质量，建立信任循环

#### 3.1 自动化测试覆盖

- 关键用户旅程 100% 测试覆盖
- 测试可被 Agent 自动运行
- 失败测试有清晰的错误信息和修复指导
- 偶发失败通过重跑解决，而非无限期阻塞

#### 3.2 Agent-to-Agent 审核

高吞吐量环境下，Agent 互审成为主流：
- Agent A 提交代码 → Agent B 审核 → 自动合并
- 人类只在关键节点介入审查
- 审核 Agent 有明确的检查清单

#### 3.3 吞吐量与合并理念

```
低吞吐量环境          高吞吐量环境
严格阻塞门控    →    减少阻塞门控
人工审核为主    →    Agent 审核为主
等待成本低      →    等待成本高
纠错成本高      →    纠错成本低
```

#### 3.4 质量度量

跟踪以下指标判断 Harness 效果：
- **吞吐量**：PR 数量/天、合并时间
- **质量**：架构违规次数、返工率
- **自主性**：Agent 自主完成率、人工干预频率
- **健康度**：文档新鲜度、技术债务增长率

---

## MCP 工具集成

Model Context Protocol（MCP）是 2026 年 Agent 调用外部工具的统一标准。

**核心概念**：MCP Server 提供工具 → Agent 通过标准协议调用 → 获取结果

**常见集成场景**：
- 数据库查询（读取 Schema、执行 SQL）
- 文件系统操作（搜索、读写）
- API 调用（第三方服务集成）
- 浏览器自动化（UI 测试）

**Harness 中的 MCP 策略**：
1. 在 AGENTS.md 中列出可用的 MCP 工具
2. 在 docs/ 中记录各工具的使用约束
3. 在 CI 中验证 MCP 配置的正确性

详见 `references/mcp-integration.md`

---

## 多 Agent 协作模式

### 协作模式

1. **串行协作**：Agent A 完成 → 交接 → Agent B 继续
2. **并行协作**：多个 Agent 同时处理不同模块
3. **审核协作**：Agent A 写代码 → Agent B 审核
4. **背景任务**：后台 Agent 持续运行清理/监控任务

### 背景 Agent 任务编排

```
定期任务：
  - 每日：运行架构检查，扫描违规
  - 每周：运行文档园艺，清理过时内容
  - 每周：运行记忆清理，归档经验
  - 每月：生成质量报告，追踪趋势
```

---

## 实施工作流程

### 阶段 1：诊断（1-2 天）

评估清单（详见 `references/checklist.md`）：
- 文档体系（AGENTS.md 是否存在、docs/ 结构）
- 架构约束（分层规则、Lint 规则）
- 自动化程度（测试、CI/CD）
- 可观测性（日志、指标、UI 测试）
- 跨编辑器配置（各工具指令文件）
- MCP 工具集成状态
- Agent 记忆管理

**产出**：成熟度评分 + 问题清单 + 改进建议

### 阶段 2：设计（3-5 天）

**优先级**：
1. **P0**：AGENTS.md + docs/ 结构 + 核心架构约束
2. **P1**：CI/CD 自动化 + 文档验证 + 跨编辑器配置
3. **P2**：可观测性增强 + MCP 集成 + 记忆管理

### 阶段 3：迭代（持续）

**熵减循环**：
```
运行 Agent → 产生熵 → 定期清理 → 编码原则 → 自动修复
     ↑                                          ↓
     └──────────── 持续改进 ─────────────────────┘
```

---

## 输出规范

使用此技能时，应产出以下内容之一：

1. **诊断报告**：当前工程环境评估 + 改进建议
2. **设计方案**：文档结构 + 架构约束 + 自动化流程 + 跨编辑器配置
3. **实施计划**：分阶段路线图 + 优先级排序
4. **实施成果**：AGENTS.md + docs/ + Lint 规则 + CI 配置

所有产出物必须：
- 可执行、可验证
- 版本化在代码仓库内
- 对 Agent 可读
- 包含反馈回路设计

## 注意事项

1. **不要过度设计**：从最小可行 Harness 开始，逐步迭代
2. **不要忽视品味**：人类品味需编码到工具和文档中
3. **不要一次性完成**：Harness Engineering 是持续过程
4. **不要外置知识**：所有知识必须内化到代码仓库
5. **不要忽视跨编辑器兼容**：AGENTS.md 是基座，工具专属文件是增强

## 参考资源

- [OpenAI Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- `references/checklist.md` - 完整检查清单
- `references/golden-principles.md` - 黄金原则
- `references/cross-editor-guide.md` - 跨编辑器配置指南
- `references/mcp-integration.md` - MCP 工具集成指南
- `assets/agents-template.md` - AGENTS.md 模板
- `assets/claude-md-template.md` - CLAUDE.md 模板
- `assets/cursor-rules-template.mdc` - Cursor Rules 模板
- `assets/github-actions-template.yml` - CI 配置模板
