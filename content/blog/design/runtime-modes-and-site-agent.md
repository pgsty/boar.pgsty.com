---
title: 'DN-007: Runtime modes and Site Agent'
description: One source tree, separate stores and failure domains, no arbitrary remote execution.
date: 2026-08-24
lastmod: 2026-09-08
weight: 70
categories: [Architecture]
tags: [server, local, sqlite, site-agent, mtls]
series: [Control Plane v2]
---

## Decision

Server, Local, and Site Agent ship from the same Go source tree but are distinct
failure domains.

- Server uses PostgreSQL for shared kernel state.
- Local uses an independent SQLite implementation of the minimal Store port.
- Site Agent owns a remote identity and connects outbound to Server with mTLS.
  Full Plan dispatch is a v1.0 target, not a current product claim.

The AI component is called Assistant. “Agent” in the product means Site Agent;
historical code identifiers such as `AgentBridge` remain frozen for
compatibility.

## Why Local has its own store

Making the legacy PostgreSQL store support SQLite through pervasive dialect
branches would couple Local to old Console tables and weaken the kernel port.
Instead, the architecture freezes the minimal Resource/Plan/Operation Store
contract and tests PostgreSQL and SQLite implementations against the same
behavior.

Local is not an in-memory demo. Its current SQLite runtime owns durable typed
Direct and export Operations, locks, events, audit, idempotency, and recovery.
It is single-user and loopback-only by design; that local OS-user policy is not
the same as Server's multi-user approval model.

## Site Agent trust model

The Agent starts with an owner-private local configuration and key. An approved
one-time enrollment turns that bootstrap into a persistent mTLS identity. The
Server binds identity to workspace, site, and action scope.

The connection is outbound so a managed site does not need a general inbound
remote-execution port.

## No `exec(command string)`

The intended execution channel accepts a versioned typed action plus a closed
payload. Local allowlists and protocol schemas reject unknown actions and
fields. Shell, Ansible, or SQL mechanics may exist only inside reviewed action
implementations.

This is not merely input sanitization. The absence of an arbitrary execution
primitive is the security boundary.

## Current Site Agent boundary

The product-wired `boar agent` runtime currently implements initialization,
one-time enrollment, and periodic identity verification. A successful grant
still reports `executionAvailable=false`; it proves neither action execution
nor Plan dispatch.

The repository also contains the K7 prototype contracts and libraries for an
SQLite execution journal, lease/reconcile transport, and typed filesystem or
systemd actions. In that prototype, the journal commits request identity and
possible-send state before action execution, and preserves terminal or UNKNOWN
evidence across partitions. Those components are historical engineering
evidence, not proof that the current Server dispatches arbitrary Kernel steps
to the product Agent. P14 is the accepted roadmap item that makes Site Agent a
Plan dispatch channel.

Automatic re-enrollment and action redispatch after an ambiguous possible-send
are forbidden. Reconciliation may read retained evidence, but it does not turn
uncertainty into a retry. Identity and execution uncertainty fail closed.

## Deployment consequence

Topology changes without changing the northbound concepts. Local can create a
populated migration bundle and Server can analyze and apply it through an
independent review. This is a controlled import, not a byte-for-byte move of
shared state: secrets, encrypted envelopes, and executable history are
excluded; credentials require rebinding and Capability is recomputed. Site
Agents can be added for identity today, while remote Plan dispatch remains P14.

Operator reference: [Runtime modes](/docs/start/runtime-modes/) and
[Site Agent](/docs/manage/site-agent/).

## Sources in the current repository

- `cmd/boar/cmd/root.go`, `cmd/boar/cmd/local.go`, and
  `cmd/boar/cmd/siteagent.go` — the three current CLI entry points.
- `internal/localruntime/state.go`, `internal/localruntime/worker.go`, and
  `internal/kernelstore/sqlite/` — the Local SQLite runtime and worker.
- `internal/localruntime/migration_bundle.go`,
  `internal/handler/local_import.go`, and
  `internal/server/local_import_runtime.go` — bounded export and reviewed
  Server import.
- `internal/siteagent/runtime/README.md` — current product enrollment/identity
  limit and `executionAvailable=false` result.
- `internal/siteagent/journal/`, `internal/siteagent/execution/`, and
  `internal/siteagent/action/` — prototype journal, transport, and typed-action
  components.
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md` — P14
  product dispatch target.
