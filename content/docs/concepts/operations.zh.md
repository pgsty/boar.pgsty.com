---
title: 操作与事件
description: 用持久状态、诚实恢复和可重放证据执行密封计划。
weight: 40
---

Operation 是一份已准入 Plan 的持久化执行，不是 UI Job，也不是内存中的 Goroutine。

## 权威模型

Kernel Store 持有 Operation、Step、Event、Approval、Lock、Lease 与 Idempotency 状态。
Worker Protocol 在调用外部系统前，先提交建立执行所有权的状态转换。

```text
准入 Plan
  → 创建 Operation 与初始 Event
  → 取得 Resource Lock 与 Worker Lease
  → 持久提交 RUNNING / Step Commitment
  → 调用类型化 Driver
  → Verification
  → Terminal Outcome 与 Audit
```

## 崩溃行为

恢复依据最后一个持久化 Commitment 与 Provider Evidence：

- 外部调用承诺之前，Step 可以按 Lease Protocol 安全重新领取。
- 即使外部调用可证明幂等，重放仍必须由 Action 合同显式允许。
- 如果调用可能已发送且无法验证，结果必须是 UNKNOWN。
- 模糊写入永不自动重试。

Resource Lock 防止不兼容 Operation 并发。Cancellation 是带有明确终态的持久化请求；
HTTP 断开不会静默取消已确认操作。

## Event 与重放

Operation Event 必须有序、持久、可重放。Transport 只是 Adapter：当前系统使用版本化
WebSocket Envelope 与分页 REST Replay。以后增加 SSE 不会改变 Event Authority。
产品视图可以限制一次 Response 并明确提示截断；持久 Event 总数与 Operation 终态不会
被当前显示的 Slice 取代。

## Job 是投影

历史 `jobs` 表继续承载 Console 与 Chat 投影；新的 `operations`、`operation_steps` 与
`operation_events` 才是执行权威。历史 Job 不会被改写成虚构的 Operation。

设计理由见 [DN-004](/zh/blog/design/immutable-plan-durable-operation/) 与
[DN-005](/zh/blog/design/unknown-is-a-first-class-result/)。
