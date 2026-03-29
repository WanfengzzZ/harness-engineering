# Harness Engineering Skill

## 概述

这个 Skill 基于 OpenAI 内部验证的 Harness Engineering 实践，为 Agent 构建高效可工作的工程环境。

**核心理念**：给 Agent（干活的牛马）套上 Harness（马具，让它能真正干活的整套工程结构）。

## 安装

### 方式 1：手动安装

将 skill 目录复制到你的 skills 目录：

```bash
# CodeBuddy
cp -r harness-engineering ~/.codebuddy/skills/

# Cursor
cp -r harness-engineering ~/.cursor/skills/

# 其他编辑器请参考对应文档
```

### 方式 2：使用包管理器（推荐）

```bash
# 未来支持
skill install openai/harness-engineering
```

安装完成后，AI 编辑器会自动加载此 Skill。

## 使用场景

当遇到以下情况时使用此 Skill：

1. **Agent 工作效率低**：怀疑是工程环境问题而非模型问题
2. **需要优化代码仓库结构**：使 Agent 能够自主导航
3. **需要建立 AI 可读的文档体系**：而非仅对人可读
4. **需要设计自动化反馈回路**：CI/CD、自动测试、代码检查
5. **需要提高 Agent 自主工作能力**：减少人工干预

## 核心产出

使用此 Skill 可产出以下内容：

### 1. 诊断报告
- 当前工程环境评估
- 成熟度评分
- 改进建议（按优先级排序）

### 2. 设计方案
- 文档结构设计（`docs/` 目录）
- AGENTS.md 编写指南（~100 行地图）
- 架构约束定义
- 自动化流程设计

### 3. 实施计划
- 分阶段路线图
- P0/P1/P2 优先级排序
- 预计时间投入

### 4. 实施工具
- 自定义 Lint 脚本（`scripts/architecture-lint.py`）
- 文档验证脚本（`scripts/validate-docs.py`）
- AGENTS.md 模板（`assets/agents-template.md`）
- 黄金原则文档（`references/golden-principles.md`）

## 使用示例

### 示例 1：诊断当前环境

```
使用 harness-engineering skill，帮我诊断当前代码仓库的
工程环境成熟度，找出 Agent 工作效率低的根本原因。
```

### 示例 2：设计 Harness 方案

```
我们准备启动一个新项目，希望从一开始就按照 Harness 
Engineering 的原则来设计工程环境。请帮我设计完整的
Harness 方案，包括文档结构、架构约束、自动化流程等。
```

### 示例 3：实施改进

```
根据 Harness Engineering 的原则，帮我们实现以下改进：
1. 创建 AGENTS.md 文件
2. 设计 docs/目录结构
3. 编写架构依赖检查脚本
4. 建立文档验证流程
```

### 示例 4：优化现有项目

```
我们已有一个大型项目，但 Agent 工作效率不高。请用 
Harness Engineering 的方法帮我们优化现有工程环境，
提高 Agent 的自主工作能力。
```

## 核心原则

### 原则 1：代码仓库即记录系统
所有知识必须版本化存储在代码仓库内，而非外部系统。

### 原则 2：为 Agent 可读性优化
Agent 运行时无法访问的上下文 = 不存在。

### 原则 3：规范架构与品味
通过强制执行不变量，而非微观管理实现。

### 原则 4：提高应用可读性
让 Agent 能够直接读取 UI、日志、指标，自主 QA。

### 原则 5：吞吐量改变合并理念
高吞吐量环境下，减少阻塞门控，Agent 对 Agent 审核。

## 参考文档

- `references/checklist.md` - 完整检查清单
- `references/golden-principles.md` - 黄金原则
- `assets/agents-template.md` - AGENTS.md 模板

## 工具脚本

- `scripts/architecture-lint.py` - 架构依赖检查
- `scripts/validate-docs.py` - 文档验证

## 成功指标

使用此 Skill 后，应看到以下改进：

1. **吞吐量提升**：PR 数量/天/工程师增加
2. **质量提升**：架构违规次数减少，返工率下降
3. **自主性提升**：Agent 自主完成率提高，人工干预减少
4. **健康度提升**：文档新鲜度提高，技术债务增长率下降

## 注意事项

1. **不要过度设计**：从最小可行 Harness 开始，逐步迭代
2. **不要忽视品味**：人类品味需编码到工具和文档中
3. **不要一次性完成**：Harness Engineering 是持续过程
4. **不要外置知识**：所有知识必须内化到代码仓库

## 案例参考

OpenAI 内部实验成果：
- 3 人团队，5 个月，100 万行代码
- 1500 个 PR，平均每人每天 3.5 个 PR
- 全程无人工代码，全部由 Codex 编写
- 产品有真实日活用户

详细案例参考：https://openai.com/zh-Hans-CN/index/harness-engineering/

## 版本

- 版本：1.0.0
- 许可证：MIT
- 基于：OpenAI Harness Engineering 实践
- 贡献：欢迎提交 PR 和 Issue

## 开源信息

- **仓库**：https://github.com/openai/harness-engineering
- **问题反馈**：https://github.com/openai/harness-engineering/issues
- **文档**：https://openai.com/zh-Hans-CN/index/harness-engineering/

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 社区

- 加入讨论：GitHub Discussions
- 关注更新：Releases
- 分享案例：Issues

---

**声明**：本 Skill 基于 OpenAI 公开的 Harness Engineering 实践整理，旨在帮助开发者更好地应用这一工程方法。
