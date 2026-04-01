# Agent 工作指南

> 本仓库遵循 Harness Engineering 原则。这是你的工作地图（~100 行）。

## 快速开始

1. **阅读核心文档**（~10 分钟）
   - [核心架构](docs/design-docs/core-beliefs.md)
   - [架构地图](ARCHITECTURE.md)
   - [当前计划](docs/exec-plans/active/)

2. **检查环境**
   ```bash
   npm run lint && npm test
   ```

3. **工作流程**：理解需求 → 实现 → 测试 → 自检 → 提交 PR

## 架构规则

**分层依赖**（只能向前依赖）：
```
Types → Config → Repo → Service → Runtime → UI
横切关注点通过 Providers 注入
```

**禁止事项**：
- 反向依赖（如 Service 引用 UI）
- 硬编码配置
- 非结构化日志（使用 logger，不用 console.log）
- 跳过测试提交

## 文档导航

| 类别 | 位置 |
|------|------|
| 设计文档 | `docs/design-docs/` |
| 产品规格 | `docs/product-specs/` |
| 执行计划 | `docs/exec-plans/active/` |
| 参考文档 | `docs/references/` |
| 黄金原则 | `docs/references/golden-principles.md` |
| 技术债务 | `docs/exec-plans/tech-debt-tracker.md` |

## 质量标准

提交 PR 前确认：
- [ ] 代码通过 lint 和 typecheck
- [ ] 测试通过，新功能有测试覆盖
- [ ] 相关文档已同步更新
- [ ] 遵循架构分层规则

## 常用命令

```bash
npm run dev          # 开发服务器
npm run lint         # 代码检查
npm test             # 运行测试
npm run typecheck    # 类型检查
npm run build        # 构建
```

## 反馈回路

遇到问题？
1. 文档缺失 → 创建文档
2. 工具缺失 → 开发工具
3. 规则缺失 → 编写 Lint 规则
4. 测试缺失 → 补充测试

---

**最后更新**：[日期] | **版本**：1.0
