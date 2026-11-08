---
title: 'DN-006：三个管理域，一套派发权威'
description: 保留 PostgreSQL、Patroni、Pigsty 语义，但不保留三条写入路径。
date: 2026-08-24
lastmod: 2026-09-08
weight: 60
categories: [架构]
tags: [postgresql, patroni, pigsty, 驱动]
series: [Control Plane v2]
---

## 三个管理域

Boar 通过三类不同运行权威管理 PostgreSQL：

- Direct SQL 与 PostgreSQL Protocol 行为；
- Patroni REST/DCS 的 HA Cluster 语义；
- Pigsty Inventory 与白名单 Lifecycle Automation。

不能把它们压成一个通用 `exec` API：每个域的 Identity Evidence、Idempotency、Failure
Boundary、Risk 与 Verification 都不同。

但保留三条独立写路径同样危险：Policy、Approval、Audit 与 Crash Recovery 会逐渐漂移，
Assistant 或 Legacy Endpoint 也可能绕过最强的执行通道。

## 决策

Provider 语义保留在 Typed Driver；Resource、Capability、Plan、Policy、Operation 与 Audit
共享。同一 Domain 对外只能有一套 Dispatch Authority。

```text
Kernel Step
   ├─ Patroni Driver → REST / DCS / PostgreSQL Verification
   ├─ PostgreSQL Driver → Typed SQL Action / Parameter Verification
   └─ Pigsty Driver → Sealed argv / Lifecycle Postcondition
```

## Patroni

仓库公共 Package 是 Canonical Implementation。既有 `control.Plan/v1alpha1` 成为 Typed
Driver Payload；19 条 CLI 与 Differential Oracle 永久保留。Adapter 保持行为，但不能
绕过 Kernel Operation 调用 Patroni。

## PostgreSQL

Direct Discovery 生成 Resource/Capability Fact。Write 必须是 Create Index、Parameter
Change 等具体 Action，而不是任意 SQL String。Parameter Plan 知道变更是 Dynamic、需要
Reload 还是需要 Restart。

## Pigsty

Inventory Import 生成 Candidate Graph。Driver Plan 绑定 Source Digest、Cluster、Host、
Limit、Tag 与封闭 Extra-variable Allowlist。执行 argv 由经过审查的代码生成，不接受 GUI
提供的 Command 或 Playbook。

## 迁移与投影

Legacy Route 可以为兼容保留，也可以接收 Job Projection。Feature Gate 在 Cutover 期间
选择唯一 Authority，不授予权限，也不能导致 Dual Dispatch。

旧 Job 可以引用新 Operation，但不能持有第二次执行。

这条规则约束 Mutation。读侧采集可以通过有界 Reader 直连 PostgreSQL、Patroni 或已配置的
Metric Provider；ADR-023 也明确要求 Boar 自己提供可扫一眼的仪表与问题面板。这不会形成
第二套写入权威。

## 当前实现边界

当前仓库包含 Typed PostgreSQL Write、Patroni Action 与 Pigsty Lifecycle 的 Kernel
Runtime，也保留 Compatibility Adapter 与 Legacy Job Projection。Console 是否显示某个
Action，仍取决于当前 Effective Capability 与 Policy。产品路线图按用户旅程分期：v0.7
聚焦只读驾驶舱，v0.8 聚焦有闸门的可逆变更，v0.9 才进入破坏性 Pigsty 深度。因此 Driver
已经存在，不代表每个 UI 或每个已发布版本都已经暴露其全部动作。

## 结果

系统共享治理与恢复，同时保留管理域原生事实。这正是“一套控制面”的核心：统一的是语义，
而不是用同一个无类型机制抹平差异。

操作参考：[驱动](/zh/docs/concepts/drivers/)、[Patroni](/zh/docs/manage/patroni/)与
[Pigsty](/zh/docs/manage/pigsty/)。

## 当前仓库依据

- `BOAR-CHARTER.md`：CKR 写路径、Driver 与 Typed Action 不变量。
- `internal/adapter/controlruntime/provider.go` 与 `control/`：Patroni Compatibility
  Adapter 与 Canonical Public Behavior。
- `internal/server/postgres_write_kernel_runtime.go`、
  `internal/server/patroni_kernel_runtime.go` 与
  `internal/server/pigsty_kernel_runtime.go`：当前三个管理域的 Runtime。
- `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`：
  ADR-023 与 ADR-024。
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`：当前产品列车范围与
  验收顺序。
