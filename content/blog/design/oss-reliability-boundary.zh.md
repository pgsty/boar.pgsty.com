---
title: 'DN-011：开源可靠性边界'
description: License 可以限制组织复杂度，但不能限制控制 PostgreSQL 所必需的安全能力。
date: 2026-08-24
lastmod: 2026-09-08
weight: 110
categories: [产品]
tags: [开源, 企业版, license, 可靠性]
series: [Control Plane v2]
---

## 决策

核心可靠性永久开源。License 可以限制组织复杂度与合规集成，但不能关闭让 PostgreSQL 控制
保持安全的机制。

## 冻结的版本边界

- Local、Server Runtime 与 Direct Connection；
- Resource、Capability、Planner、Operation 与 Audit；
- 核心 PostgreSQL、Patroni、Pigsty、PIG/SOW 与 pgBackRest Driver；
- 基本 RBAC 与 Approval；
- Site Agent 与本地账户；
- MCP Read 与 Plan。

这些不是试用层，而是 CKR-016 与 ADR-011 要求的产品 Reliability Substrate。这份清单固定
版本归属，不表示围绕每个组件的后续路线图旅程都已交付。例如仓库已有 Site Agent Prototype，
但完整派发通道、Air-gap/NAT 旅程与客户端生成仍是 v1.0 路线图 P14–P15 的工作。

## Enterprise 可以包含

多 Organization 强隔离、SAML/SCIM、高级 OIDC、HA Control-plane Deployment、外部
KMS/HSM、WORM/SIEM Integration、多级 CAB、Fleet Federation、签名 Plugin Certification
与商业支持属于 Enterprise 边界。

区别在于 Organization/Compliance Scale，而不是 Operator 是否有权取消危险 Operation 或
查看 Audit Trail。

## 当前过期行为

License Expiry 不能破坏：

- Running/Unknown Operation 的安全恢复；
- Reject 与 Policy Enforcement；
- Cancellation；
- Core OSS Control Write；
- Verification 与 Audit。

历史 `control_write` Gate 已从当前核心可靠性路径移除。对 `expired` 与 `inactive` 状态，
`internal/license/service.go` 当前只返回 `session_message_write` 一项限制。核心确认、批准、
拒绝、取消、用户管理与控制写入均不在该限制集合中；Handler 测试覆盖了恢复与核心批准场景。

这项残留限制对应可选的 Legacy Console Assistant 消息写入路径。它是当前实现行为，不表示
全部 Assistant 功能都属于 Enterprise。任何未来版本归属仍须遵守 CKR-016 的更窄规则：
License 只能 Gate 组织复杂度与合规能力。

Kernel 与 Public Package 不允许 Import License，因此商业决策不能成为隐藏的执行依赖。

## License Framework 仍然有用

Boar 保留 Offline ES256 Verification、Optional Local Issuing、Durable License State 与
进程内 Evaluated-snapshot Cache。Activation 与 Issuing 需要认证和 Legacy `manage_access`
权限（授予 `admin` 与 `workspace_admin`），受 Rate Limit 保护，并尝试写入 Audit；Audit Insert
失败只记日志，不会回滚成功请求。这些机制足以清晰表达 Enterprise Boundary；架构限制的是
它们可以 Gate 什么。

## 产品结果

版本合同允许用户在 OSS 中评估和运行真实控制面。正式发布状态与路线图完成度另行记录；
本决策本身不会把本地验收工件提升成公开 Release。Enterprise 价值应来自更大的组织与合规
Surface，而不是安全恢复数据库的权利。

管理参考：[许可证与版本边界](/zh/docs/admin/licensing/)。

## 依据

- 规范性 OSS/Enterprise 边界：`BOAR-CHARTER.md`（CKR-016、CKR-017、§7）与 `_bmad-output/planning-artifacts/control-plane-decision-log.md`（ADR-011）。
- 当前限制集合与 Cache 行为：`internal/license/service.go`、`internal/license/cache.go`。
- 当前 Route、RBAC、Rate Limit 与 Audit Wiring：`internal/handler/routes.go`、`internal/handler/license.go`、`internal/store/license.go`。
- License 过期回归行为：`internal/license/service_test.go`、`internal/handler/middleware_test.go`。
- Site Agent 完成边界：`_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`（P14–P15）。
