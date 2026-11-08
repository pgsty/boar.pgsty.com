---
title: Status and roadmap
description: The verified Boar implementation snapshot and the product-first train from v0.7 through v1.0.
weight: 5
---

This page separates implemented and accepted behavior from work in progress and
future plans. It was checked on **2026-09-08** against the Boar source tree and
its acceptance evidence.

> [!IMPORTANT]
> The v0.7 cockpit has passed local acceptance, but it has not been pushed or
> formally released. Its signed artifacts use the `local-acceptance` scope and
> must not be treated as public release artifacts.

## Current status

| Train | Scope | Status on 2026-09-08 |
|---|---|---|
| v0.3–v0.6 | Kernel, three-domain unification, Local and Site Agent prototypes, backup/observe, Console read model | Delivered in the source train; their historical contracts remain regression evidence |
| v0.7 | Read-only cockpit, P0–P5 | All six Epics passed local real-target journeys, `make test`, `make lint`, the release contract gate, and local four-platform artifact verification; not formally released |
| v0.8 | Reversible operations, P6–P10 | Development is in progress; no v0.8 acceptance directory existed at this snapshot, so no Epic or release completion is claimed |
| v0.9 | Destructive Pigsty lifecycle, P11–P13 | Planned |
| v1.0 | Site Agent dispatch and automation, P14–P15 | Planned |
{.wide .expand}

“Read-only cockpit” names the train's primary operator surfaces, not a claim
that the whole program performs no writes. v0.7 also contains bounded,
Plan-governed connection saves, member binding, session cancel/terminate, and
an optional Grafana annotation output. The three kernel write-channel switches
default to enabled; Effective Capability and Policy still govern each action.

## v0.7 acceptance snapshot

The accepted source is
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac`. The six accepted Epics are:

| Epic | Accepted operator outcome |
|---|---|
| P0 — Gate cleanup | Everyday `make test` and `make lint` are separated from the release-only contract gate, while historical manifests remain protected |
| P1 — Fleet and timeline | Fleet health, changes, operations, backups, Patroni history, and Grafana annotations can be followed through one timeline |
| P2 — Direct PostgreSQL | Local and RDS-like direct targets expose overview metrics, activity, lock waits, configuration, Top SQL, and an audited cancel path |
| P3 — Health report | Eight classes of real findings, export, and user-supplied TCO comparison were exercised against a deliberately misconfigured target |
| P4 — Protection view | Topology, replication, routing, pool state, and recoverable backup window are visible, including direct collection without a monitoring stack |
| P5 — Pigsty read view | Inventory drift and structured lifecycle progress were replayed against real Pigsty targets |

The final gate recorded 817 frontend tests, a clean `make lint`, and one clean
`make check-contract` after the Epic journeys. Four platform archives were
built twice and verified byte-for-byte with checksums, SBOMs, and an Ed25519
signature. Runtime coverage has two explicit limits: Linux arm64 was compiled
and signature-verified without a runtime environment, and Darwin amd64 ran
through Rosetta. Linux amd64 and Darwin arm64 ran natively.

The full evidence and limitations live in the source repository's
[v0.7 acceptance record](https://github.com/pgsty/boar/blob/c6afd5b9b6d3d722dc6cd791996fa4a0c33d984f/docs/acceptance/v0.7/README.md).
The evidence commit was still local at this snapshot, so the link becomes
available only after that commit is pushed. The product source identified by
that evidence remains `3094b048…`.

## Product-first train

The current delivery authority is the accepted
`control-plane-roadmap-v0.7-v1.0.md`, authorized by CC-CP-007 and ADR-022 through
ADR-025. Product definition and the Charter's 20 CKRs remain unchanged. The
older numbered PRD, architecture, K1–K11 stories, and v0.2 contracts remain
historical and traceability sources.

- **v0.7, read-side trust:** fleet and timeline, direct DBA views, health
  reports, protection views, and Pigsty inventory/progress.
- **v0.8, reversible gates:** environment and change policy, temporary access,
  cluster governance, first-class Patroni operations, alerts, command palette,
  OpenAPI coverage, and approved MCP apply.
- **v0.9, destructive lifecycle:** inventory editor and drift convergence, SOP
  templates, and job recovery drills.
- **v1.0, agent and automation:** production Site Agent dispatch and the
  constrained junior-DBA account with generated clients.

## Acceptance rules from v0.7 onward

Each Epic closes with one end-to-end journey against a real target plus clean
`make test` and `make lint` runs. Tests are added after the journey works and
cover kernel invariants and the journey; added test lines stay at or below one third
of added product lines. `make check-contract` runs once at release time.
Historical story receipts, compatibility manifests, and contract checks remain
preserved, but new work does not create a checker and receipt set for every
Story.

The kernel axioms remain unchanged: every write has an immutable Plan;
Effective Capability alone controls action availability; UNKNOWN stays
distinct and terminal; ambiguous writes are not retried automatically; durable
commit precedes the provider call; the GUI exposes no arbitrary shell or
Ansible; AI cannot approve; and credentials are never stored in plaintext.
