---
title: 运行模式
description: 按状态所有权与故障域选择 Server、Local 和 Site Agent。
weight: 30
---

Boar 使用同一份 Go 源码树和发行线，但不同 Runtime 位于不同故障域。

| 模式 | 持久化 Kernel Store | 适用场景 | 网络边界 |
|---|---|---|---|
| Server | PostgreSQL 元数据库 | 共享控制平面与 Console | 接收入站 HTTP；由 Server 或 Agent 访问 Provider |
| Local | 独立 SQLite 数据库 | 单用户工作站或封闭 Appliance | 只允许回环 HTTP |
| Site Agent | 本地身份与执行日志 | 在远端站点内受控执行 | 通过出站 mTLS 连接 Server |
{.wide .expand}

## Server Mode

`boar server` 在 PostgreSQL 中保存共享 Resource、Plan、Operation、Approval 与
Audit。历史裸 `boar` 调用只是兼容 Adapter，不是第二套 Runtime 实现。

当你需要多 Principal、共享 Console、远端站点或中央审计权威时，使用 Server Mode。

## Local Mode

`boar local` 是真实控制平面，不是内存 Demo。它用 SQLite 实现同一份最小 Kernel Store
合同，并在精确回环地址上服务内嵌 UI。Local Bootstrap 面向单用户，主动拒绝远程绑定。

Local Mode 不需要 Pigsty Lifecycle 也有完整价值：直连 PostgreSQL 发现与安全控制是它的
第一等旅程。

## Site Agent

Site Agent 是执行通道，不是 AI Assistant。当前 CLI 已实现私有初始化、一次性获批
Enrollment、mTLS Identity 验证与安全 Journal 查看。此时 `boar agent run` 的含义是
“必要时 Enrollment 一次，然后用 mTLS Identify”，还不是 v1.0/P14 计划中的持久远程
Dispatch Loop。

目标设计只接受类型化白名单动作，并在网络分区期间维护 Execution Journal。

它不暴露 `exec(command string)`，也不会成为独立 Planner。Resource、Capability、Plan、
Policy、Operation 与 Audit 权威仍由 Server 持有。

## Assistant

Assistant 是 Console Feature 内的 Actor。它依据显式 `ai.*` Capability 进行读取、解释、
诊断和请求计划，但没有 Raw Shell、Raw SQL Write、Approval 或 Force 权限。

设计理由见[运行模式与 Site Agent](/zh/blog/design/runtime-modes-and-site-agent/)。
