---
title: 仓库架构
description: 定位公共合同、Kernel、Provider、Server 与 Console。
weight: 10
---

Go Module 是 `github.com/pgsty/boar`。公共 Package 定义可复用合同与 Provider Algorithm；
`internal/` 持有 Server 具体装配。

## 公共核心

| 领域 | Package |
|---|---|
| Resource Model | `resource`、`capability`、`model` |
| Plan 与执行 | `plan`、`operation`、`driver`、`kernelstore` |
| Patroni Domain | `patroni`、`dcs`、`dcs/etcd3`、`postgres`、`control` |
| Schema | `schema/**/v*`、`api/openapi.yaml` |

公共合同 Package 不依赖 Console、License、LLM、Web 或 Legacy Metadata Table。

## Server 与 Feature Layer

- `cmd/boar` 是 Cobra 入口。
- `internal/server` 组合 HTTP Lifecycle、Store、Driver、Worker 与内嵌前端。
- `internal/handler` 持有 HTTP 与 WebSocket Adapter。
- `internal/store` 保留历史 PostgreSQL Metadata Store。
- `internal/consoleview`、`internal/postgresdba`、`internal/postgresactivity`、
  `internal/postgreshealth`、`internal/clustertopology`、`internal/clustermetrics`、
  `internal/pigstyview` 与 `internal/pigstyprogress` 实现 v0.7 读侧 Projection 与问题面板。
- Provider 相关 Internal Package 实现 Connection、Discovery、Credential、Policy、Local
  与 Site Agent Runtime Wiring。
- `frontend/` 是 React 19 Console。
- `internal/migrate/migrations/` 及其中的 `LATEST.sql` 快照持有前向 PostgreSQL Schema 演进。
- `compatibility/` 与 `test/contracts/` 持有冻结 Manifest 与 Evidence Receipt。

## 依赖方向

```text
handler → service/engine → typed tool 或 kernel service → store/driver
```

公共 Model 保持数据与校验合同。下层不能依赖 Console，也不能把 UI Decision 当成授权。

## 前端

Console 使用 React 19、TypeScript Strict、React Router 7、React Query 5、Zustand、
Radix/shadcn Primitive、Tailwind、Lucide 与 i18next。用户可见文本必须进入翻译资源。
应用支持配置 Basename 与内嵌生产构建。当前视觉系统亮色优先、由 Token 驱动，并以
`data-mode` 为后续暗色模式预留入口。

## Runtime Store

Server 用 PostgreSQL 保存共享 Kernel State；Local 用独立 SQLite 实现最小 Kernel Store
Port。历史 PostgreSQL Store 不会变成跨 Dialect 抽象。
