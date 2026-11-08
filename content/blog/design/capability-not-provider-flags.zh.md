---
title: 'DN-003：使用 Capability，而非 Provider Flag'
description: 为什么动作可用性必须经过评估、可以解释，并由所有入口共享。
date: 2026-08-24
lastmod: 2026-09-08
weight: 30
categories: [架构]
tags: [能力, 策略, 交互, 授权]
series: [Control Plane v2]
---

## 问题

Provider 驱动的界面很容易硬编码：“Provider 是 Patroni 就显示 Failover”“来自 Pigsty 就
显示 Backup”。这些判断把产品分类、目标支持、传输可用性、Credential、Permission、
Current State 与 Policy 混成一个脆弱条件。

结果是同一个 Action 在 CLI、Console、API 与 Assistant 中表现不同，而且隐藏按钮不会
告诉 Operator 原因。

## 决策

Boar 建模两层能力：

- **Intrinsic Capability**：Resource 与类型化 Driver 原则上能支持什么。
- **Effective Capability**：当前 Principal 是否能在当前 Resource 上执行此 Action，并
  返回显式 Reason Code。

Intrinsic Evaluator 消费 Provider、Interface、Version、Topology、Current State 与
Prerequisite 等类型化 Observation。独立的 Scoped Policy Projection 再应用 Principal 与
Resource Scope、Channel、Risk、Approval、MFA、Maintenance Window 和 Lock Requirement。
各个 Action 可以增加类型化的 Relationship、Connection、Credential、Identity 与 Freshness
前置条件，但不能从 Provider Name 推断这些条件。

在 Capability v1 协议中，`support` 只能是 `supported`、`unsupported`、`unknown` 或
`insufficient_privilege`。`intrinsic` 与 `effective` 是可空布尔值，因此未知结论不会被
折叠成 `false`。缺失的 Privilege Probe 不能在没有证据时变成授权或拒绝。

## Capability 不等于执行

Effective Capability 显示“可用”，只表示 Action 可以进入 Planning，不授权无 Plan 的
Provider Call。生成的 Plan 仍要绑定精确 Input、Risk、Precondition、Policy 与 Target
Version。

反之，“不可用”也是结构化结果，不是一段 Disabled CSS。例如：

- Observation Fact 缺失、过期或因权限不足无法取得；
- 没有 Verified Connection 或可用 Credential；
- Topology 或 Provider Version 超出支持边界；
- Principal 未激活或 Resource Scope 不足；
- Policy 按 Action、Risk、Environment 或 Channel 拒绝；
- 需要 Confirmation、Approval、Resource Lock、Maintenance Window 或 MFA。

## 所有 Surface 使用同一个答案

Server Resource API 当前返回 Intrinsic Snapshot 与单独的、感知 Policy 的 Effective
Projection，Console 使用这份权威。保留的 Patroni-compatible CLI 仍有自己的公共
`control.Service` 与本地评估边界；MCP apply 全覆盖排在 v0.8 P10，而不是当前已经完成。
架构不变量是这些 Surface 最终遵守同一套 Resource、Capability、Plan、Policy 与 Audit
语义，并不表示每个 Client 今天都在调用 Resource API Endpoint。

这也让扩展更简单：新 Driver 向 Evaluator 提供 Typed Action 与 Fact，而不是让每个 UI
Surface 都学习新的 Provider Name。

## Risk 仍由 Kernel 持有

Driver 可以声明支持 Action，但不能降低 Kernel Risk。Legacy Provider Declaration 与
Action-risk Registry 冲突时，采用更严格等级。

操作参考：[能力](/zh/docs/concepts/capabilities/)。

## 依据

- `BOAR-CHARTER.md`（CKR-010）
- `capability/types.go`
- `internal/capabilityengine/evaluate.go`
- `internal/scopedpolicy/capability.go`
- `internal/resourceapi/types.go`
- `cmd/boar/cmd/patronictl_runtime.go`
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`（P10）
