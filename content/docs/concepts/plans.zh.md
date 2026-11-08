---
title: 计划与策略
description: 把执行意图绑定为不可变、可审查的制品。
weight: 30
---

Boar 中的每个副作用都从 Kernel Plan 开始。所谓“直接执行”的低风险动作，只是 Policy
可以自动批准的单步骤 Plan。

v0.7 验收保留冻结的历史 Plan Schema，并为新增 Action 提供独立的 v0.7 Schema Profile；
旧 Plan Byte、Approval 与 Operation 均未被改写。截至 2026-09-08，v0.8 治理源码仍在
开发，尚无完成的 Epic 或列车验收。

## Plan 绑定什么

密封的 `plan/v1` 绑定：

- 目标 Workspace、Resource UID、Generation 与 Etag；
- Action、Risk、到期时间、Preconditions 与 Warning Codes；
- 类型化 Intent 的 Schema Version、Schema Digest 与规范化输入；
- `capabilityHash` 与 `policyHash`；
- Step Graph，包括 Driver 与 Action 版本、目标、输入 Digest、`payloadRef`、
  Verifier Reference/Digest、Risk 与 Reversibility。

完整 Hash 与 Plan ID 从规范化的权威字段派生。可执行 Driver 内容通过 `payloadRef`
引用并由 Digest 绑定，不以内联任意 SQL、Argv 或 Command String 表达。申请人与创建
时间保存在 `internal/nativeplan.Record` 等外围准入记录中；可读摘要属于投影。
它们不是 `plan/v1` Decoder 接受的附加字段。

任何执行相关字段变化都会得到新的 Plan Hash，并令审批失效。Driver Payload 对随意修改
保持不透明，但仍受 Action 的封闭 Codec 与 Schema 校验。

## Plan 血统

仓库中存在几种历史 Plan：

| 名称 | 角色 |
|---|---|
| Kernel Plan `plan/v1` | 资源级北向继任合同 |
| Patroni Control Plan `control.Plan/v1alpha1` | 由 Adapter 嵌入的冻结 Provider 原生计划 |
| Legacy Tool Plan | Console Assistant 历史路径，副作用出口迁往 Kernel |
| Pigsty Driver Plan | 绑定 Source Digest 的 Driver Payload |

继任模型保留已经验证的 Provider 语义，不会就地改写冻结的 v1alpha1 Schema。

## Policy 准入

Policy 根据 Principal、Resource Scope、Risk、Approval State、Freshness、Capability 与
Active Lock 评估不可变 Plan。Admission 是独立的持久化决策；创建 Plan 不等于执行。

新 HTTP API 使用 Idempotency Key 与 Conditional Request 保护准入；旧 Endpoint 通过
Adapter 获得等价保护。

设计理由见 [DN-004：不可变计划与持久操作](/zh/blog/design/immutable-plan-durable-operation/)。

依据：Boar 仓库的 `plan/types.go`、`plan/codec.go` 与 `internal/nativeplan/types.go`。
