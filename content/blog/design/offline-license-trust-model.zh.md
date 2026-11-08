---
title: 'DN-014：离线 License 信任模型'
description: 分离公钥验签、可选签发、持久状态与产品门控。
date: 2026-02-13
lastmod: 2026-09-08
weight: 140
categories: [安全]
tags: [license, jwt, es256, 密钥]
---

## 决策

Boar License 是在本地验证的 ES256 JWT。Validation 不发起网络请求，使用内嵌 Public Key
以及额外配置的 Verification Key。Issuing 是可选能力，只有配置 Private Key 且其公钥与
Verifier 中至少一把公钥匹配时才存在。

## Claim

Validator 接受 Pig 兼容 Subject 形式 `type=<license_type>,node=<node_limit>`，也接受显式
`license_type` / `node_limit` 字段。当前代码的 Fallback 是成对进行的：只有
`license_type` 为空时才解析 Subject，并同时赋值 Type 与 Node Limit。如果
`license_type` 已存在，代码不会读取 Subject，`node_limit` 保留显式值或 JSON 零值。

Token 只允许 ES256，并强制 `exp`、`iat`、`nbf`。Validation 使用 UTC Wall Clock，Leeway
为 30 秒。`iss` 与 `aud` 都必须非空，但 Validator 不会与配置的 Allowlist 比对。负 Node
Limit 在 Subject Fallback 得出最终值后直接拒绝。签发的 Token 带随机 `jti`；Validation
不要求 `jti`，也不按它撤销 Token。

## Key 分离

Verification Key 来自内嵌默认值，加上配置的 Public-key PEM 文本或文件路径。验证或激活
License 永远不需要 Private Key。

License PEM Loader 接受 Inline PEM，或对传入路径直接调用 `os.ReadFile`。它没有执行 Boar
部分其他 Credential-key Loader 所做的 Owner、Mode 或 Symlink 检查，因此部署侧文件保护
不属于这段 License Loader 的保证。

没有 Private Key 时，Optional Issue Endpoint 不可用。配置 Private Key 后，Startup 检查其
公钥是否属于 Verification Set，Server 还会立即验证每个刚签发的 Token。对该 Endpoint，
`month=0` 会把 `exp` 写成 2200-12-31；它仍是普通 Expiry Claim，不是特殊的无过期 JWT 类型。

这消除了常见歧义：“Private-key Injection”属于 Issuing；Verification 始终使用 Public Key。

## 持久状态

PostgreSQL 中单行 `license_state` Record 保存 Trial/Active/Expired/Inactive State、Type、
Node Limit、Expiry、Trial Window、Normalized Claim 与 Update Time。没有 Record 时创建并
持久化七天 Trial。该行不保存原始 License Token 或签名 Private Key。

Status 需要 Authentication。Activation 与 Issuing 还要求 Legacy `manage_access` 权限（授予
`admin` 与 `workspace_admin`），并受 Rate Limit 保护。Handler 会调用 Audit Insert Helper，
但 Audit Insert 失败只记日志，不会回滚已经成功的请求。Issue Endpoint 面向管理/脚本，不是
默认 End-user UI。

`node_limit`、`features` 与 Normalized Claim 当前会被解析或存储；License Service 尚不按这些
Claim 执行节点数或 Feature 名称限制。`expired` / `inactive` 当前只限制可选的
`session_message_write` 路径。

## 时间与撤销边界

“Offline”只表示签名和时间 Claim 在本地验证。当前实现没有 Online Entitlement Lookup、
Revocation List、Trusted-time Service、Monotonic-clock Journal 或通用 Anti-rollback Check。
Token 与 Trial 过期依赖宿主机 Wall Clock；已持久化为 `expired` 的状态会保持过期，但这不是
完整的防时钟回拨机制。Activation 也不会把有效 Token 与上一个已存 Token 比较，因此不会
阻止安装一份更旧但仍有效的 License。

License 的 ES256 签名与 Release Evidence 是两套机制。v0.7 本地验收工件使用 Ed25519 对
`SHA256SUMS` 签名，并声明 `signatureScope=local-acceptance`；它不签署源码树、不赋予公开
Release Identity，也不改变 License Validation。

## 产品边界修正

早期实现曾按 License State Gate 一些写入能力。Control Plane v2 Charter 将 Licensing
允许控制的范围收窄为组织复杂度与合规 Feature。Core Reliability、Safe Recovery、
Rejection、Cancellation 与 OSS Control 在过期后仍须可用。

这不会推翻 JWT Trust Model，只改变哪些 Consumer 可以使用 License State。

管理参考：[许可证与版本边界](/zh/docs/admin/licensing/)。

## 依据

- Claim、成对 Subject Fallback 与 PEM Loading 边界：`internal/license/claims.go`、`internal/license/validator.go`。
- 签发日期与 `jti`：`internal/license/issuer.go`。
- Trial、Expiry、Cache 与当前限制消费方：`internal/license/service.go`、`internal/license/cache.go`。
- Durable Row：`internal/migrate/migrations/0005_add_license_state.sql`、`internal/store/license.go`。
- Startup 密钥匹配、Endpoint Auth、Rate Limit 与 Audit 行为：`internal/server/server.go`、`internal/handler/routes.go`、`internal/handler/license.go`。
- 产品边界：`BOAR-CHARTER.md`（CKR-016、CKR-017、§7）。
- 独立的 v0.7 工件签名 Scope：`docs/acceptance/v0.7/README.md`、`docs/acceptance/v0.7/release/boar-v0.7.0-build-receipt.json`。
