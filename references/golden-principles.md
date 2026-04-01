# 黄金原则 v2.0

> 7 条核心原则，保持代码库对 Agent 可读、可维护。
> 违反处理：轻微→自动修复 | 中度→警告+手动修复 | 严重→阻塞 CI

## 原则 1：共享工具优先

**规则**：优先使用共享 utility 包，禁止重复造轮子。

```typescript
// ❌ 手工实现并发控制
async function processWithConcurrency(items, limit) { ... }

// ✅ 使用共享工具
import { concurrentMap } from '@/utils/concurrent';
await concurrentMap(items, processItem, { concurrency: 5 });
```

**实施**：建立 `@/utils/` 共享包，Lint 推荐使用。

## 原则 2：禁止 YOLO 式探测

**规则**：禁止基于猜测访问数据，必须验证边界或使用类型化 SDK。

```typescript
// ❌ YOLO
const value = data.nested.property.value;

// ✅ 边界验证
const validated = validateData(data);
const value = validated.nested.property.value;
```

**实施**：提供验证工具包 + 类型化 SDK，Lint 检查未验证的链式访问。

## 原则 3：结构化日志

**规则**：所有日志必须结构化，包含 trace_id。

```typescript
// ❌
console.log('User logged in:', userId);

// ✅
logger.info('user.logged_in', { userId, trace_id: getTraceId() });
```

**实施**：Lint 禁止 console.log，提供统一 logger。

## 原则 4：分层依赖

**规则**：代码只能向前依赖，禁止反向。

```
Types(0) → Config(1) → Repo(2) → Service(3) → Runtime(4) → UI(5)
横切关注点通过 Providers 注入
```

**实施**：`scripts/architecture-lint.py` 自动检查，CI 阻塞违规。

## 原则 5：文档与代码同步

**规则**：过时文档比没有文档更糟。代码变更 7 天内必须更新文档。

**实施**：
- `scripts/validate-docs.py` 检查文档年龄和断链
- CI 验证文档同步
- doc-gardening Agent 定期扫描

## 原则 6：错误处理一致性

**规则**：错误必须结构化，包含错误类型和修复指导。

```typescript
// ❌
throw new Error('Something went wrong');

// ✅
throw new AppError({
  code: ErrorCode.USER_NOT_FOUND,
  message: '用户不存在',
  fix: '检查用户 ID 是否正确',
});
```

**实施**：定义统一错误类型，Lint 检查裸 Error。

## 原则 7：配置外部化 + 单一职责

**规则**：
- 配置禁止硬编码，统一通过 `@/config` 管理
- 文件 < 300 行，函数 < 50 行
- 命名遵循统一约定

**实施**：Lint 检查文件大小、硬编码、命名模式。

---

## 定期审查

每季度审查：
1. 原则是否仍然适用？
2. 是否需要新增/调整？
3. Agent 遵循度如何？

黄金原则是活文档，随团队和 Agent 成长而演进。
