---
title: Local Mode
description: 使用仅 Owner 可访问的 SQLite Store 运行同一套控制面 Kernel。
weight: 40
---

Local Mode 是单用户故障域，在仅 Owner 可访问的 SQLite Store 上运行 Kernel，无需共享
PostgreSQL 元数据服务。

> [!NOTE]
> 截至 2026-09-08，SQLite Store、Guarded Bootstrap、Direct Onboarding、无 Secret
> Export 与多平台本地验收已经实现。v0.7 P2 还证明了 Local 的 SQL 工作区和本地查询
> 历史，但没有验收完整 Local 仪表或 Session Control；v0.7 尚未正式发布。

## 启动

```bash
make build
install -d -m 0700 "$PWD/.local/boar"
./bin/boar local --state-dir "$PWD/.local/boar" --listen 127.0.0.1:0
```

Local 需要 `make build` 产出的内嵌前端二进制。普通的非内嵌 `go run` 构建因为没有 Local
Frontend，会 Fail Closed。

State Directory 必须是绝对路径且仅 Owner 可访问，Listener 必须是 Loopback。
`127.0.0.1:0` 会选择随机端口，避免与 Server 实例冲突。

Local Bootstrap 创建一个 Owner Authority 与 Guarded Browser Session，不会静默复用
Server Credential，也不会绑定环境中的任意网络接口。

## Store 一致性

SQLite 是最小 Kernel Store Port 的独立实现，不会把 SQL Dialect 分支塞进历史 PostgreSQL
`internal/store`。参数化 Contract Test 覆盖共享 Resource、Plan、Operation、Event、
Lock、Approval、Idempotency 与 Lost-ack 不变量。

## Export

```bash
./bin/boar local export --help
```

Export 本身也是经过 Plan 与 Audit 的 Action。导出格式不包含 Secret Material，并保持
稳定 External Identity。

## 边界

- Local 是单用户模式，不是缩小版多租户 Server。
- 远程绑定 Fail Closed。
- Direct Onboarding、SQL 工作区与本地 History 可用。
- 不能从共享 UI 推断完整 Server 仪表或 Session Action 已在 Local 对齐。
- Site Agent 与中央多 Principal Approval 属于 Server Mode。
