# 黄金原则（Golden Principles）

> 这些原则是带有主观意见的机械规则，旨在保持代码库的可读性和一致性，以便将来运行的 Agent 能够有效工作。
> 
> 基于 OpenAI 内部实践总结的 10 条核心原则。

## 原则 1：共享工具优先

**规则**：优先使用共享的 utility 包，而非手工编写的辅助工具。

**理由**：
- 不变式集中管理
- 行为可预测
- 易于维护和测试
- Agent 更容易理解

**示例**：
```typescript
// ❌ 错误：手工编写的并发控制
async function processWithConcurrency(items, limit) {
  // 手工实现的并发控制逻辑
  // 容易出错，难以测试
}

// ✅ 正确：使用共享工具包
import { concurrentMap } from '@/utils/concurrent';
await concurrentMap(items, processItem, { concurrency: 5 });
```

**实施**：
1. 建立共享 utility 包
2. 编写完整测试（100% 覆盖率）
3. 集成到文档系统
4. 通过 Lint 推荐使用

## 原则 2：禁止 YOLO 式探测

**规则**：禁止基于猜测的结构构建，必须验证边界或使用类型化的 SDK。

**理由**：
- 防止 Agent 基于错误假设构建
- 早期发现数据结构变化
- 减少运行时错误

**示例**：
```typescript
// ❌ 错误：YOLO 式探测
const data = await fetch('/api/data');
const value = data.nested.property.value; // 可能 undefined

// ✅ 正确：边界验证
import { validateData } from '@/utils/validation';
const data = await fetch('/api/data');
const validated = validateData(data); // 失败时抛出明确错误
const value = validated.nested.property.value;

// ✅ 正确：类型化 SDK
import { DataService } from '@/services/data';
const data = await DataService.get(); // 类型安全
const value = data.nested?.property?.value;
```

**实施**：
1. 提供验证工具包
2. 提供类型化 SDK
3. Lint 检查未验证的访问
4. 错误信息包含修复指导

## 原则 3：结构化日志

**规则**：所有日志必须结构化，包含 trace_id 和 span_id。

**理由**：
- 便于 Agent 查询和分析
- 支持分布式追踪
- 符合可观测性标准

**示例**：
```typescript
// ❌ 错误：非结构化日志
console.log('User logged in:', userId);

// ✅ 正确：结构化日志
import { logger } from '@/utils/logging';
logger.info('user.logged_in', {
  userId,
  timestamp: new Date().toISOString(),
  trace_id: getTraceId(),
  span_id: getSpanId(),
  metadata: {
    ip: request.ip,
    userAgent: request.headers['user-agent']
  }
});
```

**实施**：
1. 提供结构化日志工具
2. 自动注入 trace_id/span_id
3. Lint 检查 console.log 使用
4. 定义标准日志格式

## 原则 4：分层依赖规则

**规则**：代码只能向前依赖，禁止反向依赖。

**依赖方向**：
```
Types → Config → Repo → Service → Runtime → UI
         ↓          ↓         ↓         ↓
      Providers（横切关注点）
```

**示例**：
```typescript
// ❌ 错误：Service 层直接依赖 UI 组件
import { UserCard } from '@/ui/components/UserCard';

// ✅ 正确：通过 Providers 注入
import { UIProvider } from '@/providers/ui';
export class UserService {
  constructor(private ui: UIProvider) {}
}
```

**实施**：
1. 自定义 Lint 检查依赖
2. CI 阻塞违规提交
3. 错误信息包含修复建议
4. 定期扫描技术债务

## 原则 5：文档与代码同步

**规则**：文档必须与代码同步更新，过时文档比没有文档更糟。

**理由**：
- Agent 依赖文档导航
- 过时文档导致错误决策
- 技术债务累积

**实施**：
1. CI 验证文档同步
2. doc-gardening Agent 定期扫描
3. 自动发起修复 PR
4. 严重过期时阻塞合并

**检查规则**：
- 代码变更后 7 天内文档必须更新
- API 变更必须同步更新文档
- 架构调整必须更新架构文档

## 原则 6：测试覆盖关键路径

**规则**：所有关键用户旅程必须有自动化测试覆盖。

**定义关键路径**：
- 用户注册/登录
- 核心功能使用
- 支付/交易
- 数据持久化

**实施**：
1. 定义关键路径清单
2. 编写端到端测试
3. CI 强制运行
4. 监控测试稳定性

## 原则 7：错误处理一致性

**规则**：错误处理必须一致，包含明确的错误类型和修复指导。

**示例**：
```typescript
// ❌ 错误：随意抛出错误
throw new Error('Something went wrong');

// ✅ 正确：结构化错误
import { AppError, ErrorCode } from '@/utils/errors';
throw new AppError({
  code: ErrorCode.USER_NOT_FOUND,
  message: '用户不存在',
  cause: originalError,
  fix: '检查用户 ID 是否正确，或先创建用户',
  context: { userId }
});
```

**实施**：
1. 定义错误类型系统
2. 提供错误处理工具
3. Lint 检查裸 Error 使用
4. 错误信息包含修复指导

## 原则 8：配置外部化

**规则**：所有配置必须外部化，禁止硬编码。

**理由**：
- 便于环境切换
- Agent 可动态调整
- 安全性提升

**示例**：
```typescript
// ❌ 错误：硬编码配置
const API_URL = 'https://api.example.com';
const TIMEOUT = 5000;

// ✅ 正确：配置外部化
import { config } from '@/config';
const API_URL = config.api.url;
const TIMEOUT = config.api.timeout;
```

**实施**：
1. 统一配置管理
2. 环境变量注入
3. 配置验证
4. 禁止硬编码 Lint

## 原则 9：单一职责

**规则**：每个文件、函数、类只负责一件事。

**检查标准**：
- 文件大小 < 300 行
- 函数长度 < 50 行
- 类的方法 < 10 个

**实施**：
1. 文件大小 Lint
2. 函数复杂度检查
3. 超阈值时建议重构

## 原则 10：命名一致性

**规则**：命名必须遵循统一约定，反映业务领域。

**示例**：
```typescript
// ❌ 错误：随意命名
function getData() { }
function fetchData() { }
function retrieveData() { }

// ✅ 正确：统一命名
// Repository 层：findByX, save, update
// Service 层：getUserWithProfile, createOrder
// UI 层：useUserQuery, useOrderMutation
```

**实施**：
1. 命名约定文档
2. Lint 检查命名模式
3. 代码审查把关

## 违反处理流程

```
发现违反 → Lint 警告 → 自动修复（如可能） → 创建技术债务记录 → 定期清理
```

**自动化程度**：
- 轻微违反：自动修复
- 中度违反：警告 + 手动修复
- 严重违反：阻塞 CI + 立即修复

## 定期审查

每季度审查黄金原则：
1. 是否仍然适用？
2. 是否需要新增？
3. 是否需要调整？
4. Agent 是否遵循？

黄金原则是活的文档，随团队和 Agent 的成长而演进。
