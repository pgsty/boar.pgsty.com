---
title: 'DN-005：UNKNOWN 是第一等结果'
description: 为什么 SDK、API、Operation、Audit 与 UI 都必须保留不确定性。
date: 2026-08-24
lastmod: 2026-09-08
weight: 50
categories: [可靠性]
tags: [未知, 重试, 验证, 安全]
series: [Control Plane v2]
---

## 危险的简化

分布式写入存在一个无法消除的情形：请求可能已经越过边界，但 Client 丢失 Response。
报告“失败”看似方便，却会诱导自动重试，重复执行 Failover、Restart、DCS Delete、SQL
Change 或 Lifecycle Action。

Boar 拒绝这种简化。

## 三条独立轴

每个终态 Mutation Result 分别记录三个事实：

- **Outcome**：`SUCCEEDED`、`FAILED` 或 `UNKNOWN` 业务结果。
- **SendState**：`NOT_SENT`、`MAYBE_SENT`、`ACCEPTED` 或 `REJECTED` 传输事实。
  `ACCEPTED` 与 `REJECTED` 是精确传输结果，不是笼统的“已经发送”。
- **Verification**：`CONFIRMED` 或 `UNCONFIRMED`。成功与失败由 Outcome 表达；
  Verification 没有 `CONTRADICTED` 协议值。

规范的模糊结果是：

```text
UNKNOWN / MAYBE_SENT / UNCONFIRMED
```

它不是加了装饰的 Error，而会改变允许的 Recovery Behavior。

真值表还允许 `UNKNOWN / ACCEPTED / UNCONFIRMED`，以及唯一狭窄的非传输例外：带
`CONCURRENT_CONFLICT` 的 `UNKNOWN / NOT_SENT / UNCONFIRMED`。这些是经过校验的不同
Tuple，不是描述性文案。

## 禁止盲目重试

模糊写入永不自动重试。恢复必须依靠以下一种证据：

- Provider 定义的 Idempotency Contract；
- 直接 Postcondition Verification；
- 能证明调用未发送的 Durable Journal；
- Operator 显式对账后创建新 Plan。

Retry Decision 属于 Typed Action 与 Operation Recovery Model，不能交给 HTTP Client
Library 或通用 Queue。

## 贯穿整个系统

UNKNOWN 在 Public Go Type、JSON Schema、API Response、CLI Machine Output、Operation
Event、Audit、Legacy Job Projection 与 Console 中保持不变。即使后端 Record 正确，UI
若把它涂红并标成“Failed”也违反合同。

同一原则适用于 Discovery：“无法观察”不等于“不存在”。Unknown 是对证据边界本身的证据。

## 事故行为

Operation 为 UNKNOWN 时：

1. Worker 不自动重放；Operator 也应在对账前暂停依赖它的破坏性动作；
2. 保存 Plan、Step、Event、Driver 与 Transport Evidence；
3. 必要时检查 Provider 与 Site Agent Journal；
4. 记录 Reconciliation Evidence；
5. 只有在当前状态足够清楚后，才创建新 Plan。

这比二元成功/失败需要更多 Operator 关注，但这是控制有状态基础设施必须诚实支付的成本。

操作参考：[错误与结果语义](/zh/docs/reference/errors/)。

## 依据

- `BOAR-CHARTER.md`（CKR-004、CKR-005）
- `control/types.go`
- `operation/state.go`
- `operation/types.go`
- `internal/kernelworker/recovery.go`
- `internal/kernelworker/runner.go`
