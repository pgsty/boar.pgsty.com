---
title: 许可证与版本边界
description: 理解 ES256 License State，同时不让许可证关闭开源可靠性。
weight: 40
---

Boar 保留 JWT License Framework，但 Control Plane v2 冻结了清晰产品边界：可靠性与核心
控制面安全永久属于开源版本。

## License Token

License Token 使用 ES256。Verification 接受配置的 Public Key；可选 Issue 流程需要独立
Private Key。持久 `license_state` Record 保存 Activation State 与 Token Metadata，原始
Private Signing Material 永远不进入数据库。

API 提供 Status、Activate，以及仅在配置 Issuing Key 时可用的 Issue 流程。License 变更
必须经过 Authentication、Authorization、Rate Limit 与 Audit。

激活与签发 Handler 会尝试写入审计，但当前审计插入失败只记录日志，不回滚请求。
这不等同于 Kernel 的 Operation/Event/Audit 原子提交保证。签名验证要求 Issuer 与
Audience 非空，但不会与配置的身份允许列表匹配；详见
[离线许可证信任模型](/zh/blog/design/offline-license-trust-model/)。

## OSS 边界

Charter 将下列能力永久划归 OSS。这是版本归属边界，不代表每条规划中的工作流均已实现：

- Local 与 Server Mode；
- Resource、Capability、Planner、Operation 与 Audit；
- 核心 PostgreSQL、Patroni、Pigsty、PIG/SOW 与 pgBackRest Driver；
- 基本 RBAC 与 Approval；
- Site Agent；
- 本地账户；
- MCP 的八个模型可调用 Read、Diagnose、Plan Create 与 Plan Explain 工具。

Enterprise 可以增加多 Organization 强隔离、SAML/SCIM、高级 OIDC、HA Control Plane、
外部 KMS/HSM、WORM/SIEM 合规、多级 CAB、Fleet Federation、签名插件认证和商业支持。

这些是允许商业化的范围，不是已交付集成清单。当前交付边界见
[状态与路线图](../../develop/roadmap/)与 [Site Agent 原型](../../manage/site-agent/)。

Assistant Facade 还定义 Approval Request 与 Apply Approved Action，但两者均为
`modelCallable=false`；MCP 模型不能批准或应用 Plan。

## 可靠性不变量

License 不能关闭安全恢复、拒绝、取消或核心控制面。Kernel 与 Public Package 不依赖
License、Console、LLM、Web 或 Legacy Metadata。历史 `control_write` Feature Gate 不能
成为关闭 OSS 可靠性的总开关。

当前 Server 的初始试用期为七天。过期或未激活状态只限制 `session_message_write`，
由 `POST /api/sessions/:sid/messages` 上的门禁执行。核心控制写入、确认与用户管理
没有列入 `RestrictedFeatures`，不能用假定的 Enterprise 功能矩阵代替这项实际行为。

过期不能让正在运行的 Operation 无法验证或无法安全取消。Local 不消费 Server 的
License Gate。

设计理由见 [DN-011：开源可靠性边界](/zh/blog/design/oss-reliability-boundary/)。

依据：Boar 仓库的 `BOAR-CHARTER.md` §7、`internal/license/service.go`、
`internal/handler/routes.go` 与 `internal/handler/middleware.go`。
