---
title: Quick start
description: Run Boar from source and verify the first read-only surface.
weight: 10
---

This quick start targets a local development workstation and the source tree as
of 2026-09-08. It does not describe a production deployment.

## Prerequisites

- Go `1.26.6` for the current Boar source tree.
- Node.js `26.4.0` and npm for the React frontend.
- PostgreSQL 18 with a metadata database named exactly `boar` when using Server mode; the v0.7 local journey used `18.6`.
- A recent Git checkout of `github.com/pgsty/boar`.

> [!WARNING]
> The metadata database is not a managed application database. Never point
> Boar migrations at a PostgreSQL database that contains application data.

## Start Server mode with the Console

The simplest development path starts Vite on port 5173 and the Go server on
port 9876:

```bash
make dev
```

Open `http://127.0.0.1:5173/`. Vite serves the React application and proxies
`/api` to the backend at `127.0.0.1:9876`. On an empty metadata database, Boar
redirects to `/setup`. Create the first administrator with a username, email
address, and password, then sign in at `/login`. There is no default
administrator or default administrator password.

To run only the backend explicitly, use:

```bash
go run ./cmd/boar server \
  --database-url 'postgres:///boar?sslmode=disable' \
  --server-addr '127.0.0.1:9876'
```

A non-embedded source build serves the API and a backend information page; it
does not serve or proxy the React application. Start Vite separately and open
port 5173 if you use this command. The bare `boar` invocation currently starts
the same Server runtime, but new scripts should use `boar server` explicitly.

## Start Local mode

Local mode requires an embedded-frontend binary. Build it first, then give the
independent SQLite kernel store an absolute, owner-private state directory:

```bash
install -d -m 0700 "$PWD/.local/boar"
make build
./bin/boar local \
  --state-dir "$PWD/.local/boar"
```

Local defaults to `--listen 127.0.0.1:0`, chooses a free port, and opens a
browser. Use `--no-open-browser` for headless validation. A guarded
`--bootstrap-file` is accepted only together with `--no-open-browser`. Boar
rejects a non-loopback Local bind rather than silently exposing the
single-user control plane. `go run ./cmd/boar local` is a non-embedded build
and exits because the Local frontend is unavailable.

## Verify before connecting a target

Read the process health and version surfaces first:

```bash
curl --fail --silent http://127.0.0.1:9876/api/v1/health
curl --fail --silent http://127.0.0.1:9876/api/v1/version
```

A development server may report degraded Assistant health when Claude Code is
not installed; metadata and typed-control health remain independently visible.

## Next

1. Read [runtime modes](../runtime-modes/) before selecting a production topology.
2. Review [configuration](../configuration/) and replace every development secret.
3. Learn [resources and identity](../../concepts/resources/) before importing or connecting a target.
4. Read the [security model](../../admin/security/) before enabling a write lane.
