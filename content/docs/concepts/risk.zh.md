---
title: 风险与审批
description: 使用一套保守风险刻度，并把审批绑定到精确计划。
weight: 50
---

Kernel Risk 按具体动作定级并严格有序：

| 风险 | 旧映射 | 代表动作 |
|---|---|---|
| Read | L1 | Topology、Log、Metric |
| Low | L2 | Session Cancel、Reload、元数据纳管 |
| Medium | L3 | Session Terminate、Restart、动态参数 |
| High | L4 | Switchover、Reinitialize、Add Replica |
| Critical | L5 | Failover、Promote/Demote、Remove 或 Destroy |
| BreakGlass | 无 | 当前没有注册到此等级的 Action |

L1–L5 映射仅用于翻译冻结的历史记录，不能降低 Kernel Action Classification。不同声明
发生冲突时，Boar 一律采用更严格等级。

例如，历史路径中的 `patroni_failover` 曾声明为 L4，而 Kernel 固定为 Critical；
`patroni_edit_config` 至少为 High，并按受影响字段升格到 Critical。

Server Mode 的 `kernel_patroni_restart`、`kernel_patroni_domain` 与
`kernel_postgres_write` 默认都是 `true`。这只允许通道进入 Capability 与 Policy 评估，
不会自动批准动作，也不会绕过精确 Plan 准入。

## 审批绑定

Approval 绑定完整 Plan Hash、Approver Principal、Scope、Policy 与时间。Plan、Action
Version、Target Evidence、Expected Resource Version 或相关 Policy State 变化后，审批
立即 Stale。

历史双管理员 L5 机制成为一种 Policy 实现；Approval 不再只属于 Console Job。

## Principal 分离

提出 Plan 的 Actor 不会自动获得审批权。尤其是 AI Principal 与 Approver Principal 必须
分离。Charter 中的 Assistant 能力词汇使用 `ai.*`，而不是 L1–L5。当前模型可调用的
范围只有读取、诊断、创建和解释 Plan。`plan.request_approval` 与 `plan.apply_approved`
仅存在于受控 Assistant Facade，且 `modelCallable=false`。
`ai.auto_remediate_low` 是规划能力，当前工具清单中不存在。参见 [HTTP API](../../reference/api/)。

## BreakGlass

BreakGlass 是显式新增类别，不是“Critical 再多一个复选框”。它要求独立 Policy Path、
例外证据与已注册的类型化 Action。当前已有这个词汇，但 Action Registry 没有把任何
Action 定为 BreakGlass。普通 GUI 与 Site Agent 都不提供任意 Shell。
