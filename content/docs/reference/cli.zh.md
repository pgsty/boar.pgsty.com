---
title: 命令行接口
description: 当前运行、管理、Pigsty、Site Agent 与 Patroni 兼容命令。
weight: 10
---

本页面对应 2026-09-08 的源码 CLI。实际操作时请对精确二进制执行
`boar <command> --help`；对某个发布版本而言，该二进制才是最终命令权威。

## 运行与管理

| 命令 | 用途 |
|---|---|
| `boar server` | 运行 PostgreSQL-backed 共享控制平面 |
| `boar local` | 运行单用户 SQLite 控制平面 |
| `boar agent` | 管理 Site Agent 初始化、Enrollment、Identity 与 Journal |
| `boar migrate` | 应用前向元数据迁移 |
| `boar version` | 输出 Build、Patroni 与 PostgreSQL 版本信息 |
| `boar completion` | 生成 Shell Completion |

当前裸 `boar` 调用仍是 Server 兼容路径。新自动化应显式使用 `boar server`。

## 全局 Flag

```text
--config
--database-url
--server-addr
--base-path
--mode
--log-format
--demo
--pigsty-home
--pigsty-inventory
```

## Patroni 兼容命令

Boar 为脚本兼容保留 19 条平铺命令：

| 读取与发现 | 常规写入 | 高风险与拓扑 |
|---|---|---|
| `version`、`list`、`topology`、`history`、`show-config`、`dsn`、`query` | `reload`、`restart`、`pause`、`resume`、`flush`、`edit-config` | `switchover`、`failover`、`reinit`、`remove`、`promote-cluster`、`demote-cluster` |
{.wide .expand}

所有命令都是原生 Cobra Callback，发布二进制不调用 Python 或 `patronictl`。

`boar discover` 是 Boar 额外提供的舰队发现命令，不属于冻结的 19 条 patronictl 兼容命令。

## Pigsty 命令

```text
boar pigsty parse
boar pigsty import
boar pigsty operations
boar pigsty plan ACTION
boar pigsty run ACTION
```

`run` 默认 Dry Run。`--execute` 只表示请求直接执行，在默认配置下并不足以触发写入：三条
Kernel Control 通道中任意一条开启时，命令都会拒绝执行，并要求精确 Kernel Plan 审批与
准入。三条通道默认均开启，因此正常写入应走 Console 或 API 的 Plan 流程。

## Local 命令

```text
boar local
boar local export
```

Local 接受绝对路径 `--state-dir`、精确回环 `--listen`、可选 Guarded
`--bootstrap-file` 与 `--no-open-browser`。Listen 默认值是 `127.0.0.1:0`；
`--bootstrap-file` 必须与 `--no-open-browser` 一起使用。

## Site Agent 命令

```text
boar agent init
boar agent enroll
boar agent identify
boar agent run
boar agent journal
```

所有命令通过 `--agent-config` 使用显式、仅 Owner 可访问的 Agent Configuration。
`boar agent run` 只在需要时执行一次 Enrollment，随后用 mTLS 验证 Identity；它尚未实现
计划中的持久 Dispatch Loop。

## 计划中的增量命令

冻结的 v2 CLI 合同预留增量 `boar plan` 与 `boar operation` Surface。当前 Binary 的 Root
Help 没有这两个命令。Plan 与 Operation 已可通过 Console 和 HTTP API 使用，但预留的
顶层 CLI 名称尚未交付。
