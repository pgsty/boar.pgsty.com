---
title: Local mode
description: Run the same control-plane kernel with an owner-private SQLite store.
weight: 40
---

Local mode is a single-user failure domain that runs the kernel on an
owner-private SQLite store without the shared PostgreSQL metadata service.

> [!NOTE]
> Status on 2026-09-08: the SQLite store, guarded bootstrap, Direct onboarding,
> no-secret export, and multi-platform local acceptance are implemented. In the
> v0.7 P2 journey, Local additionally proved the SQL workspace and local query
> history. Full Local instruments and session control were not part of that
> acceptance, and v0.7 has not been officially released.

## Start

```bash
make build
install -d -m 0700 "$PWD/.local/boar"
./bin/boar local --state-dir "$PWD/.local/boar" --listen 127.0.0.1:0
```

Local requires a binary built with the embedded frontend, as `make build`
produces. A plain non-embedded `go run` build fails closed because no Local
frontend is available.

The state directory must be absolute and owner-private. The listener must be
loopback. `127.0.0.1:0` selects a random port and prevents collision with a
Server instance.

Local bootstrap creates one owner authority and a guarded browser session. It
does not silently reuse a Server credential or bind to an ambient network
interface.

## Store parity

SQLite is an independent implementation of the minimal kernel Store port. It
does not force SQL dialect conditionals into the legacy PostgreSQL
`internal/store`. Parameterized contract tests cover the shared Resource,
Plan, Operation, Event, lock, approval, idempotency, and lost-ack invariants.

## Export

```bash
./bin/boar local export --help
```

Export is itself a planned and audited action. The exported representation is
designed to contain no secret material and to preserve stable external
identities.

## Boundaries

- Local is single-user; it is not a lightweight multi-tenant Server.
- Remote bind fails closed.
- Direct onboarding, the SQL workspace, and local history are available.
- Do not infer full Server instrument or session-action parity from the shared UI.
- Site Agent and centralized multi-principal approval belong to Server mode.
