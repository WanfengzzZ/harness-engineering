# CLAUDE.md 模板

> 此模板用于 Claude Code 项目配置。放置在项目根目录。
> 根据你的项目实际情况修改内容。

# 项目概述

[一句话描述你的项目]

## 技术栈

- 语言：[TypeScript / Python / Go / ...]
- 框架：[Next.js / Express / FastAPI / ...]
- 数据库：[PostgreSQL / MongoDB / ...]
- 部署：[Vercel / Docker / CloudBase / ...]

## 架构规则

### 分层依赖
```
Types → Config → Repo → Service → Runtime → UI
横切关注点通过 Providers 注入
```

### 禁止事项
- 不要直接在 Service 层引用 UI 组件
- 不要硬编码配置值
- 不要使用 console.log，使用结构化 logger
- 不要跳过测试就提交 PR

## 代码风格

- 使用 [项目风格指南] 的命名约定
- 每个文件 < 300 行，每个函数 < 50 行
- 优先使用 `@/utils/` 下的共享工具
- 错误处理使用 `AppError` 类型

## 文档导航

- 架构文档：`docs/design-docs/`
- 产品规格：`docs/product-specs/`
- API 参考：`docs/references/api/`
- 执行计划：`docs/exec-plans/active/`

## 工作流程

1. 阅读相关文档
2. 实现功能
3. 编写测试
4. 运行 `npm run lint && npm test`
5. 提交 PR

## 测试要求

- 所有新功能必须有测试
- 关键路径 100% 覆盖
- 使用 `npm test` 运行测试

## 常用命令

```bash
npm run dev        # 启动开发服务器
npm run lint       # 运行 lint
npm test           # 运行测试
npm run build      # 构建项目
```
