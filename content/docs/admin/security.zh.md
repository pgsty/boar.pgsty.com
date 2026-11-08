---
title: 安全模型
description: 保护凭据、分离 Principal，并让每次外部写入都可审计。
weight: 10
---

Boar 的安全模型从 Control-plane Kernel 开始。Authentication 与 UI Confirmation 都有
必要，但都不能弥补绕过 Plan、Policy、Operation 或 Audit 的执行路径。

## 信任边界

- **User 与 Service Principal** 向 Server 认证，并通过 RBAC 与 Policy 获得显式
  Workspace/Resource Scope。
- **Assistant Principal** 与 Approver Principal 分离，没有 Raw Shell、Raw SQL Write、
  Approval 或 Force Authority。
- **Site Agent Identity** 通过获批 Enrollment 与出站 mTLS 建立，再绑定到 Site 与
  Typed Action Scope。
- **Provider Credential** 只在专用 Credential Store 中保存 Reference 或加密数据，
  永不复制进 Resource、Plan、Event、Audit、Prompt 或 Screenshot。
- **Release Key** 与 Credential Master Key 是独立 Trust Root，不能从它们要验证的
  Artifact 反向推断可信。

## 文件与 Secret

Configuration、Service File、Passfile、TLS Private Key、Control Plan Key、Credential
Master Key 与 Signing Key 必须满足精确合同：规范普通文件、禁止 Symlink Traversal、
Owner 正确、权限严格、内容有界。

不能假设每种 Key Loader 都执行相同检查。当前 License Key Helper 接受内联 PEM 或
文件路径，读取文件时没有 Control/Credential Loader 那样的 Owner、Mode 与 Symlink
校验。部署时必须保护该来源；公私钥匹配不等于文件权限得到校验。

Request 或 Prompt Secret 是一次性且不可 Join 的。System Trust Root 与 Prompt/Request
Material 不能跨 Trust Change 变成可复用的环境 Cache。

## 传输

- PostgreSQL 优先使用 `VERIFY_FULL` / `sslmode=verify-full`。
- `VERIFY_CA`、加密但不验证，或明文访问必须有显式获批 Deviation。
- PostgreSQL Channel Binding `REQUIRE` 必须协商 `SCRAM-SHA-256-PLUS`。
- Endpoint Selection 与 Credential 保持分离；Service 或 Environment Host 不能静默替换
  所选 Patroni Member。
- Site Agent 使用出站 mTLS 与固定 Identity Lifecycle。

## 写入安全

每次 Mutation 都要求新鲜密封 Plan、Effective Capability、Scoped Principal、Policy
Admission 与 Durable Operation。Approval 绑定完整 Plan Digest。Operation 在外部调用前
提交所有权；模糊写入保持 UNKNOWN，禁止自动重试。

`kernel_patroni_restart`、`kernel_patroni_domain` 与 `kernel_postgres_write` 默认均为
`true`。它们选择 Kernel 作为写入权威，不会自动批准 Mutation。Kernel Control 开启时，
历史直接写命令会被拒绝，要求改走精确 Plan、Approval 与 Admission 路径。

## 审计完整性

Audit 仅追加。生产数据库权限应撤销 Audit Row 的 Update 与 Delete。即使执行失败或准入
被拒，Operation Event 与 Provider Evidence 也要保留。

## 事故响应

先停止新写入、隔离精确目标、撤销泄露 Credential/Key，并在 Cleanup 前保存 Binary/Config
Hash、Plan ID、Operation ID、Outcome、SendState、Verification、Event 与 Audit。按
[恢复手册](../upgrade-recovery/)处理，并在恢复写入前逐个对照 Provider 仲裁 UNKNOWN。
