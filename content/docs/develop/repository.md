---
title: Repository architecture
description: Navigate the public contracts, kernel, providers, server, and Console.
weight: 10
---

The Go module is `github.com/pgsty/boar`. Public packages define reusable
contracts and provider algorithms; `internal/` owns server-specific wiring.

## Public core

| Area | Packages |
|---|---|
| Resource model | `resource`, `capability`, `model` |
| Plan and execution | `plan`, `operation`, `driver`, `kernelstore` |
| Patroni domain | `patroni`, `dcs`, `dcs/etcd3`, `postgres`, `control` |
| Schemas | `schema/**/v*`, `api/openapi.yaml` |

Public contract packages do not depend on Console, License, LLM, Web, or
legacy metadata tables.

## Server and feature layers

- `cmd/boar` is the Cobra entry point.
- `internal/server` composes HTTP lifecycle, stores, drivers, workers, and
  embedded frontend.
- `internal/handler` owns HTTP and WebSocket adapters.
- `internal/store` preserves the legacy PostgreSQL metadata store.
- `internal/consoleview`, `internal/postgresdba`, `internal/postgresactivity`,
  `internal/postgreshealth`, `internal/clustertopology`,
  `internal/clustermetrics`, `internal/pigstyview`, and
  `internal/pigstyprogress` implement the v0.7 read-side projections and
  problem panels.
- provider-specific internal packages implement connection, discovery,
  credential, policy, Local, and Site Agent runtime wiring.
- `frontend/` is the React 19 Console.
- `internal/migrate/migrations/` and its `LATEST.sql` snapshot own
  forward-only PostgreSQL schema evolution.
- `compatibility/` and `test/contracts/` own frozen manifests and evidence
  receipts.

## Dependency direction

```text
handler → service/engine → typed tool or kernel service → store/driver
```

Public models remain data and validation contracts. A lower layer must not
import the Console or use a UI decision as authorization.

## Frontend

The Console uses React 19, TypeScript strict mode, React Router 7, React Query
5, Zustand, Radix/shadcn primitives, Tailwind, Lucide, and i18next. User-visible
text belongs in translation resources. The application supports a configured
basename and an embedded production build. Its current visual system is
light-first and token-driven, with `data-mode` reserved for later dark mode.

## Runtime stores

Server uses PostgreSQL for shared kernel state. Local uses an independent
SQLite implementation of the minimal kernel Store port. The legacy PostgreSQL
store does not become a cross-dialect abstraction.
