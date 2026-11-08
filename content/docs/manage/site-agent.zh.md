---
title: Site Agent
description: 在当前原型边界内建立出站 mTLS 站点身份。
weight: 50
---

Site Agent 是 Boar 为受控远端执行组件保留的名称，与 AI Assistant、Control-plane Server
都不同。

> [!NOTE]
> 截至 2026-09-08，仓库保留 K7 Enrollment、mTLS、Journal、Typed Action 与网络分区
> 安全原型合同。当前 CLI 的 `boar agent run` 只在必要时 Enroll，随后执行有边界的
> 只读 Identity Check；它不是通用 Worker 或 Plan Dispatch Loop。让 Site Agent 成为
> Plan 派发通道属于 v1.0 P14，尚未通过 Epic 或列车验收。

## 生命周期

```text
init → 获批 enrollment → 持久 identity → 重复 mTLS identify
```

当前 CLI 提供：

```text
boar agent init
boar agent enroll
boar agent identify
boar agent run
boar agent journal
```

必须使用显式且仅 Owner 可访问的 Agent Configuration。Bootstrap Enrollment 是一次性
权威；模糊尝试之后不会自动重试。

`agent run` 在没有 Identity 时至多 Enroll 一次，然后报告 Identity，并按配置周期重复
`identify`。Authentication 或 Transport 失败后进程退出；它不绑定监听 Socket，当前
Runtime 报告 `executionAvailable: false`。

## 信任与传输

Agent 主动发起出站连接。Enrollment 把获批 Bootstrap 转换成持久 mTLS Identity；后续
Session 证明该身份，而不是反复发送 Bootstrap Material。

Certificate、Private Key 与 Journal State 仅 Owner 可访问。Server 把 Agent Identity
绑定到 Workspace、Site、Capability 与 Action Scope。

## 类型化动作边界

原型 Protocol 与 Journal 定义版本化 Action Name、封闭 Payload、本地 Allowlist 与恢复
Evidence，永不接受 `exec(command string)`。Shell、SQL 与 Ansible 细节只能存在于经过
审查的 Typed Action 实现内部。这些合同约束未来 P14 派发，不表示当前 `agent run` 会
轮询或执行任务。

## Execution Journal

Execution Journal 原型记录 Receipt、Commitment、Send State、Result 与 Verification，
用于网络分区后对账。当前 CLI 可以用 `agent journal --request-id` 检查一条精确的安全
Record，但不会建立通用派发循环。Server Operation 与 Agent Journal 仍是独立证据权威，
Disconnect 不能伪造成功，也不能成为第二次执行的理由。

设计理由见 [DN-007：运行模式与 Site Agent](/zh/blog/design/runtime-modes-and-site-agent/)。
