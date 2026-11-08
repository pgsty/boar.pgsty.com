---
title: 'DN-004：不可变计划与持久操作'
description: 把已审查意图与执行分开，并在跨越 Provider 边界前先提交状态。
date: 2026-08-24
lastmod: 2026-09-08
weight: 40
categories: [架构]
tags: [计划, 操作, 策略, 恢复]
series: [Control Plane v2]
---

## 决策

Kernel 不变量要求 Boar 的每个副作用之前都有 Immutable Plan。原生 v2 Server Flow 密封
`boar.pgsty.com/plan/v1`，再创建或准入 Durable Operation；Operation 在 Driver 调用外部
系统之前提交执行所有权。保留的 v0.2 路径继续使用冻结的 `control.Plan/v1alpha1` 合同；
尚未接入 Server Kernel 的 Legacy Path 不能被描述成已经提供 `operation/v1` API。

“一键执行”不等于“没有 Plan”，只表示 Policy 可以自动准入单步骤 Low-risk Plan。

## 为什么 Plan 与 Operation 必须分开

Plan 是已审查意图，可以在不接触 Target 的前提下 Display、Compare、Approve、Reject 或
Stale。Operation 是实现一份精确 Plan 的持久化尝试，持有 Lock、Lease、Step、Event、
Result 与 Recovery。

把两者合并会制造两类失败：读取计划可能意外执行它，重试执行又可能静默生成不同意图。

## 不可变边界

Plan Digest 覆盖完整执行权威：Resource UID、Generation 与 ETag；Action 与 ActionVersion；
规范 Typed Intent 及其 Schema Digest；Risk 与 Expiry；CapabilityHash 与 PolicyHash；
Precondition 与 Warning Code；以及每个 Step 的 Driver/Version、Action/Version、Target、
依赖集合、ArgsDigest、内容寻址的 PayloadRef、Verifier Ref/Digest、Risk 与 Reversibility。
可执行 Payload 字节位于 `PayloadRef` 之后；Plan 密封引用与摘要，不嵌入任意命令。展示文本
由密封事实派生；修改 Summary 不能修改 Action。

Approval 绑定 Digest。任何相关变化都必须创建 Successor Plan 并重新审批。

## 外部调用之前先持久化

Worker Protocol 严格按以下顺序：

1. 准入时原子持久化 Plan、Operation、Queued Step、Resource Lock 与 Initial Event；
2. 将 Operation 转为可运行状态，并用 Worker Lease Claim 一个 Step；
3. 持久化 `RUNNING` Step 与 Dispatch Commitment；
4. 在任何 Driver I/O 前持久化 `MAYBE_SENT`；
5. 调用 Typed Driver 并取得 Typed Result，无法取得时进入 Recovery；
6. 持久化 Stage Result，包括 SendState、Verification、Evidence 与可选 Checkpoint；
7. 原子完成终态 Step/Operation、Event、Audit 与 Lock Release。

这套顺序在 Provider Contract 允许的范围内关闭“已调用 Provider，但记录前崩溃”的窗口。
无法关闭时，答案必须是 UNKNOWN，而不是虚构 Failure 后再重试。

## Idempotency 与 Lock

Idempotency Key 保护 Admission，但不会让任意 Provider Mutation 自动幂等。Resource Lock
阻止不兼容 Operation；Lease 允许 Worker Death 后恢复，同时不把所有权交给两个 Worker。

Cancellation 是持久状态转换。HTTP Disconnect 不会取消已确认 Operation，Startup 也不会
盲目重放 Pending External Write。

## 历史 Plan

`plan/v1` 作为北向合同继任 `control.Plan/v1alpha1`、Legacy Tool Plan 与 Pigsty Driver
Plan。已迁移 Flow 通过 Adapter 或内容寻址 Payload 衔接经过验证的 Typed Provider Plan，
而不修改冻结 Schema；兼容合同继续保留。

操作参考：[计划](/zh/docs/concepts/plans/)与[操作](/zh/docs/concepts/operations/)。

## 依据

- `BOAR-CHARTER.md`（CKR-001 至 CKR-005）
- `control/types.go` 与 `cmd/boar/cmd/patronictl_runtime.go`
- `plan/types.go`
- `operation/state.go` 与 `operation/types.go`
- `internal/kernelstore/postgres/operation.go`
- `internal/kernelworker/runner.go`
- `internal/kernelstore/postgres/worker.go`、`internal/kernelstore/postgres/audit.go` 与 `internal/kernelstore/postgres/worker_multistep.go`
- `internal/migrate/migrations/0012_kernel_operation_store.sql`
