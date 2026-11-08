---
title: 'DN-007：运行模式与 Site Agent'
description: 同一源码树、独立 Store 与故障域，并且没有任意远端执行。
date: 2026-08-24
lastmod: 2026-09-08
weight: 70
categories: [架构]
tags: [server, local, sqlite, site-agent, mtls]
series: [Control Plane v2]
---

## 决策

Server、Local 与 Site Agent 来自同一份 Go 源码树，但属于不同故障域。

- Server 用 PostgreSQL 保存共享 Kernel State。
- Local 用独立 SQLite 实现最小 Store Port。
- Site Agent 持有远端 Identity，通过出站 mTLS 连接 Server。完整 Plan 派发是 v1.0 目标，
  不是当前产品事实。

AI 组件称为 Assistant。产品文案中的“Agent”专指 Site Agent；`AgentBridge` 等历史代码
标识为兼容保持冻结。

## 为什么 Local 使用独立 Store

如果让历史 PostgreSQL Store 通过无处不在的 Dialect Branch 支持 SQLite，Local 会耦合
旧 Console Table，也会削弱 Kernel Port。因此架构冻结最小 Resource/Plan/Operation Store
Contract，让 PostgreSQL 与 SQLite 实现在同一套行为测试下运行。

Local 不是内存 Demo。当前 SQLite Runtime 拥有持久 Typed Direct/Export Operation、Lock、
Event、Audit、Idempotency 与 Recovery。单用户与 Loopback-only 是有意边界；Local OS User
Policy 不等同于 Server 的多用户 Approval Model。

## Site Agent 信任模型

Agent 从仅 Owner 可访问的本地 Configuration 与 Key 开始。获批的一次性 Enrollment 把
Bootstrap 变成持久 mTLS Identity；Server 把该身份绑定到 Workspace、Site 与 Action
Scope。

连接由 Agent 出站发起，因此受管 Site 不需要暴露通用入站远程执行端口。

## 没有 `exec(command string)`

预期的执行通道只接受版本化 Typed Action 与封闭 Payload。本地 Allowlist 与 Protocol
Schema 拒绝未知 Action/Field。Shell、Ansible 或 SQL 机制只能存在于经过审查的 Action
Implementation 内部。

这不仅是输入清洗；系统不存在任意执行 Primitive，本身就是安全边界。

## 当前 Site Agent 边界

当前产品接线中的 `boar agent` Runtime 只实现初始化、一次性 Enrollment 与周期 Identity
Verification。Grant 成功后仍明确返回 `executionAvailable=false`；它既不证明 Action 已可
执行，也不证明 Server 已能派发 Plan。

仓库还保留 K7 Prototype 的 SQLite Execution Journal、Lease/Reconcile Transport，以及
Typed Filesystem/Systemd Action 合同与 Library。在该 Prototype 中，Journal 会在 Action
执行前持久记录 Request Identity 与 Possible-send State，并跨网络分区保留 Terminal 或
UNKNOWN Evidence。这些组件是历史工程证据，不能用来声称当前 Server 已把任意 Kernel Step
派发给产品 Agent。让 Site Agent 成为 Plan Dispatch Channel 是已接受路线图中的 P14。

出现模糊 Possible-send 后，禁止自动 Re-enrollment 或重新派发 Action。Reconciliation 可以
读取保留的 Evidence，但不能把不确定性变成 Retry；Identity 与 Execution Uncertainty 均
Fail Closed。

## 部署结果

拓扑改变不会改变北向概念。Local 当前可以生成已填充 Migration Bundle，Server 可经独立
Review 分析并 Apply。它是受控 Import，不是 Shared State 的逐字节迁移：Secret、Encrypted
Envelope 与 Executable History 均被排除；Credential 需要重新绑定，Capability 需要重新
计算。现在可添加 Site Agent Identity，远端 Plan 派发仍属于 P14。

操作参考：[运行模式](/zh/docs/start/runtime-modes/)与
[Site Agent](/zh/docs/manage/site-agent/)。

## 当前仓库依据

- `cmd/boar/cmd/root.go`、`cmd/boar/cmd/local.go` 与
  `cmd/boar/cmd/siteagent.go`：当前三个 CLI 入口。
- `internal/localruntime/state.go`、`internal/localruntime/worker.go` 与
  `internal/kernelstore/sqlite/`：Local SQLite Runtime 与 Worker。
- `internal/localruntime/migration_bundle.go`、`internal/handler/local_import.go` 与
  `internal/server/local_import_runtime.go`：有界 Export 与经 Review 的 Server Import。
- `internal/siteagent/runtime/README.md`：当前产品 Enrollment/Identity 边界及
  `executionAvailable=false` 结果。
- `internal/siteagent/journal/`、`internal/siteagent/execution/` 与
  `internal/siteagent/action/`：Prototype Journal、Transport 与 Typed Action 组件。
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`：P14 产品派发目标。
