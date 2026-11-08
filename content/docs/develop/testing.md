---
title: Build and test
description: Run proportional gates without confusing local checks with real-environment evidence.
weight: 30
---

## Toolchain

- Go module baseline: Go `1.26.6`.
- Frontend: Node.js `26.4.0`, React `19.2.0`, TypeScript `5.9.3`, Vite `8.2.1`.
- Browser gate: Playwright `1.62.1`, Chromium `151.0.7922.34`.
- Historical contract metadata baseline: PostgreSQL `18.4`, database name
  `boar`. The v0.7 P0/P2/P4 real-target journeys used PostgreSQL `18.6`.

The documentation site has its own independent toolchain: Hugo Extended
`0.168.0`, Go `1.27.3`, and Oink `v1.5.0`.

## Everyday targets

```bash
make dev
make build
make test
make lint
```

`make test` covers Go and frontend suites. `make lint` runs Go and frontend
checks. `make build` produces an embedded frontend binary.

## Release and compatibility gates

```bash
make check-contracts
make check-contract
make test-public-core
make test-public-contracts
```

These are preserved compatibility and release checks, not everyday gates.
Run the full `make check-contract` once when closing a release train. It adds
the Charter checker to the permanent historical gates and validates preserved
receipts, manifests, schema inventory, and frozen assets. The narrower public
core and contract targets remain available for focused compatibility work.

## Real environments

From v0.7 onward, each Epic closes with one end-to-end journey against a real
target plus clean `make test` and `make lint` runs. Examples include
Patroni/etcd integration, Pigsty isolated labs, PostgreSQL direct connection,
SQLite store parity, Site Agent partitions, and Console browser journeys.

Do not replace a required lab run with mocks or a browser journey with
component snapshots. Tests are added after the journey works and cover the
journey and kernel invariants; new test lines stay at or below one third of new
product lines. Historical Story evidence remains preserved, but new work does
not create per-Story receipts and checkers.

## Database scope

Local development may use only the PostgreSQL database named `boar`. Never run
tests or migrations against another database on the cluster. Tests that create
schemas, roles, processes, sockets, or containers must prove cleanup and zero
unexplained residue.

## Network downloads

Repository policy requires the configured HTTP proxy for `go mod download`,
`go get`, `npm install`, `npx`, `pnpm install`, and other package downloads.
