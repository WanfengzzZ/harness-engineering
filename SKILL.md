---
name: harness-engineering
description: 为 Agent 构建高效可工作的工程环境。当需要优化代码仓库结构、文档组织、反馈回路、自动化流程，使 Agent 能够自主高效地完成开发任务时使用此技能。核心目标：让代码、文档、测试对 AI 可读而非仅对人可读。
---

# Harness Engineering

**Harness Engineering** 是 2026 年最重要的 AI 工程概念，由 HashiCorp 联创提出，OpenAI 通过内部实验验证。核心理念：**给 Agent（干活的牛马）套上 Harness（马具，让它能真正干活的整套工程结构）**。

## 核心认知

### 三阶段演进

1. **2024 提示词工程**：教模型听懂话，优化单次对话输入
2. **2025 上下文工程**：让模型看到全貌，构建完整信息环境
3. **2026 Harness Engineering**：给 Agent 搭整套能自己干活的工作环境

**本质区别**：
- 提示词工程 = 告诉它做什么
- Harness Engineering = 让它有工具、有规则、有反馈，能独立把活儿干完

### 核心问题

> **你是否给 AI 提供了一个它可以自我迭代的环境？**

自问清单：
- [ ] 你的架构约束是写在文档里，还是只存在于团队口头约定中？
- [ ] 你的测试能被自动运行，还是需要人手动触发？
- [ ] 你的设计决策有记录，还是散落在三个月前的聊天记录里？
- [ ] 你的代码仓库对 AI 可读吗？（不仅是人可读）

如果答案大多是后者，Agent 的能力天花板受限于你混乱的工程环境。

## 当何时使用此技能

**触发场景**：
- 需要优化代码仓库结构，使 Agent 能够自主导航和工作
- 需要建立对 AI 可读的文档体系（而非仅对人可读）
- 需要设计自动化反馈回路（CI/CD、自动测试、代码检查）
- 需要改进 Agent 工作环境的工程基础设施
- 需要提高 Agent 的自主工作能力和吞吐量
- 遇到 Agent 工作效率低，怀疑是环境问题而非模型问题

**不适用的场景**：
- 单纯的代码实现任务（应使用代码开发类技能）
- 单纯的需求分析（应使用产品需求类技能）
- 单纯的提示词优化（应使用提示词优化类技能）
- 与 Agent 工程环境无关的任务

## 核心原则

### 原则 1：代码仓库即记录系统（Repository as System of Record）

**错误做法**：
- 知识存储在 Google Docs、Notion、飞书等外部系统
- 架构决策散落在 Slack、微信群、邮件讨论中
- 依赖"口头约定"和"团队默契"

**正确做法**：
- 所有知识版本化存储在代码仓库内（`docs/` 目录）
- AGENTS.md 作为地图（~100 行），指向结构化文档
- 设计决策、产品原则、工程规范全部内化到仓库

**文档结构示例**：
```
docs/
├── design-docs/           # 设计文档目录
│   ├── index.md          # 设计文档索引
│   ├── core-beliefs.md   # 核心理念（操作原则）
│   └── ...
├── exec-plans/           # 执行计划
│   ├── active/          # 活跃计划
│   ├── completed/       # 已完成计划
│   └── tech-debt-tracker.md  # 技术债务追踪
├── generated/           # 自动生成的文档
│   └── db-schema.md     # 数据库 Schema（自动更新）
├── product-specs/       # 产品规格
│   ├── index.md
│   └── new-user-onboarding.md
├── references/          # 参考文档
│   ├── design-system-reference-llms.txt
│   ├── nixpacks-llms.txt
│   └── uv-llms.txt
├── DESIGN.md            # 设计系统总览
├── FRONTEND.md          # 前端规范
├── PLANS.md             # 计划管理
├── PRODUCT_SENSE.md     # 产品感知
├── QUALITY_SCORE.md     # 质量评分标准
├── RELIABILITY.md       # 可靠性要求
└── SECURITY.md          # 安全规范
```

**AGENTS.md 示例结构**（~100 行）：
```markdown
# Agent 工作指南

## 快速开始
本代码仓库由 Agent 自主维护。开始工作前，请阅读：
- [核心架构](docs/design-docs/core-beliefs.md)
- [分层地图](ARCHITECTURE.md)
- [当前计划](docs/exec-plans/active/)

## 文档导航
- **设计文档**: `docs/design-docs/index.md`
- **产品规格**: `docs/product-specs/index.md`
- **执行计划**: `docs/exec-plans/`
- **参考文档**: `docs/references/`

## 质量门控
- 所有 PR 必须通过 CI 检查
- 文档必须与代码同步更新
- 技术债务必须记录在案

## 反馈回路
遇到问题？检查：
1. 是否有相关文档？没有 → 创建
2. 是否有自动化测试？没有 → 添加
3. 是否有 Lint 规则？没有 → 编写
```

### 原则 2：为 Agent 可读性优化（Optimize for Agent Readability）

**关键认知**：Agent 运行时无法访问的上下文 = 不存在

**优化策略**：

#### A. 架构约束代码化
```typescript
// ❌ 错误：约束只存在于文档
// "服务层应该调用 Repository 层"

// ✅ 正确：自定义 Lint 强制约束
// .eslintrc.js
module.exports = {
  rules: {
    'layer-dependency': 'error',
    // 依赖方向：Types → Config → Repo → Service → Runtime → UI
  }
}
```

#### B. 文档可验证
```yaml
# CI 作业验证文档更新
jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - name: 检查文档与代码同步
        run: ./scripts/validate-docs-sync.sh
      - name: 检查过时文档
        run: ./scripts/find-outdated-docs.sh
```

#### C. 渐进式披露
```
Agent 从小的稳定入口开始，被指导下一步去哪，
而不是一开始就被淹没在千行文档中。

AGENTS.md (100 行) → 指向 → docs/目录 (结构化知识)
```

### 原则 3：规范架构与品味（Architectural Constraints & Taste）

**核心思想**：通过强制执行不变量，而非微观管理实现

#### 分层架构示例
```
每个业务域内（如应用设置），代码只能"向前"依赖：

Types → Config → Repo → Service → Runtime → UI

横切关注点（认证、连接器、遥测、功能标志）通过 Providers 进入。
其他任何依赖方向都不被允许，并通过自动化强制执行。
```

#### 自定义 Lint 规则
```python
# scripts/custom-linters/architecture_lint.py
# 验证分层依赖规则

from pathlib import Path

LAYER_ORDER = ['types', 'config', 'repo', 'service', 'runtime', 'ui']

def check_layer_dependencies(file_path):
    """检查文件是否违反分层依赖规则"""
    # 实现依赖方向验证
    pass
```

#### 品味不变式
```markdown
# docs/references/taste-invariants.md

## 代码品味规则

1. **禁止 YOLO 式探测数据**
   - 必须验证边界
   - 或使用类型化的 SDK
   - 禁止基于猜测的结构构建

2. **共享工具优先**
   - 使用共享 utility 包
   - 而非手工编写的辅助工具
   - 不变式集中管理

3. **结构化日志**
   - 所有日志必须结构化
   - 包含 trace_id, span_id
   - 遵循 OpenTelemetry 规范
```

### 原则 4：提高应用可读性（Increase Application Readability）

**目标**：让 Agent 能够直接读取 UI、日志、指标，自主 QA

#### A. UI 可读性
- 使应用可根据 git worktree 启动
- Agent 为每次更改启动并驱动一个实例
- 接入 Chrome DevTools 协议到智能体运行时
- 创建处理 DOM 快照、屏幕截图和导航的技能

#### B. 可观测性可读性
```python
# 本地可观测性堆栈对 Agent 可见
# Agent 可以使用 LogQL 查询日志，PromQL 查询指标
# 日志、指标和追踪记录通过临时堆栈展示
```

### 原则 5：吞吐量改变合并理念（Throughput Changes Merge Philosophy）

**高吞吐量环境的特点**：
- Pull Request 生命周期很短
- 测试偶发失败通过重跑解决，而非无限期阻塞
- 纠错成本低，等待成本高
- 智能体对智能体的审核成为主流

**对比**：
```
低吞吐量环境          高吞吐量环境
严格阻塞门控    →    减少阻塞门控
人工审核为主    →    Agent 审核为主
等待成本低      →    等待成本高
纠错成本高      →    纠错成本低
```

## 实施工作流程

### 阶段 1：诊断当前环境

**评估清单**：
```markdown
## 文档体系
- [ ] 核心架构文档是否存在且更新？
- [ ] 设计决策是否有记录？
- [ ] 文档是否版本化在代码仓库内？

## 自动化程度
- [ ] 测试是否能自动运行？
- [ ] CI/CD 是否完整？
- [ ] 代码检查是否自动化？

## 架构约束
- [ ] 分层架构是否有明确定义？
- [ ] 依赖规则是否被强制执行？
- [ ] 是否有自定义 Lint 规则？

## 可观测性
- [ ] Agent 能否访问日志？
- [ ] Agent 能否访问指标？
- [ ] Agent 能否自主测试 UI？
```

### 阶段 2：设计改进方案

**优先级排序**：
1. **P0 - 基础文档结构**：创建 AGENTS.md 和 docs/目录结构
2. **P0 - 核心架构约束**：定义分层规则并代码化
3. **P1 - 自动化反馈回路**：完善 CI/CD 和自动测试
4. **P1 - 文档验证机制**：确保文档与代码同步
5. **P2 - 可观测性增强**：让 Agent 能访问日志和指标
6. **P2 - UI 可读性**：接入 DevTools 协议

### 阶段 3：迭代优化

**熵减循环**：
```
运行 Agent → 产生熵（代码漂移） → 定期清理 → 编码黄金原则 → 自动修复 PR
     ↑                                                        ↓
     └────────────────── 持续改进 ────────────────────────────┘
```

**黄金原则示例**：
1. 优先使用共享 utility 包，而非手工辅助工具
2. 禁止 YOLO 式探测数据，必须验证边界
3. 所有日志必须结构化，包含 trace_id

**定期清理流程**：
```bash
# 每周运行后台 Agent 任务
./scripts/cleanup-ai-drift.sh
# 扫描偏差、更新质量等级、发起重构 PR
```

## 关键成功因素

### 1. 人类角色的转变

**从写代码到设计环境**：
- 人类确定方向，Agent 执行
- 工程速度提升数个数量级
- 核心工作：设计环境、明确意图、构建反馈回路

**深度优先工作方式**：
```
大目标 → 拆解为小模块 → Agent 构建 → 解锁复杂任务
         ↓
    遇到阻塞 → 退后思考：Agent 缺什么？
         ↓
    补充工具/文档/约束到代码仓库
```

### 2. 情境管理

**地图 vs 百科全书**：
- ❌ 巨大的 AGENTS.md（1000+ 行）
- ✅ 简短的地图（~100 行）+ 结构化 docs/目录

**情境稀缺性认知**：
- 情境是稀缺资源
- 过多指导反而无效
- 渐进式披露：从小入口开始，指导下一步

### 3. 技术债务管理

**认知转变**：
```
技术债 = 高息贷款

❌ 攒到还不起时被迫清算
✅ 每天还一点（持续清理）
```

**实践方法**：
- 每周五清理"AI 残渣"（占 20% 时间）→ 不可持续
- 将黄金原则编码到代码仓库 → 可持续
- 定期运行后台 Agent 任务扫描偏差 → 自动化

## 参考资源

### 核心文档
- [OpenAI Harness Engineering 原文](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [Codex CLI](https://github.com/openai/codex)

### 工具链
- 自定义 Lint 工具
- CI/CD 验证作业
- 文档园艺 Agent（doc-gardening）
- 本地可观测性堆栈

### 检查清单模板
参见 `references/checklist.md`

## 输出规范

使用此技能时，应产出以下内容之一：

1. **诊断报告**：当前工程环境评估 + 改进建议
2. **设计方案**：文档结构 + 架构约束 + 自动化流程
3. **实施计划**：分阶段路线图 + 优先级排序
4. **实施成果**：AGENTS.md + docs/目录 + 自定义 Lint 规则

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

## 典型案例

### 案例 1：新产品开发
```
场景：从零开始构建新产品
Harness 设计：
1. 初始化 AGENTS.md（100 行地图）
2. 创建 docs/目录结构
3. 定义分层架构规则
4. 编写自定义 Lint
5. 设置 CI 验证作业
6. 建立文档园艺流程
结果：3 人团队，5 个月，100 万行代码，1500 个 PR
```

### 案例 2：现有项目改造
```
场景：已有项目，Agent 工作效率低
诊断：架构约束只存在于文档，未代码化
改进：
1. 将约束编写为 Lint 规则
2. 创建 docs/目录集中文档
3. 添加文档验证 CI
4. 建立每周清理流程
结果：Agent 吞吐量提升 3 倍，返工减少 70%
```
