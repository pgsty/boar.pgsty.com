---
title: Requirements and release gates
description: Current product-train exits and the historical numbered contract that remains as traceability.
weight: 30
---

Since CC-CP-007, the authoritative schedule and acceptance model is the
product-first `control-plane-roadmap-v0.7-v1.0.md`. The Charter's product
definition and 20 CKRs remain binding. The numbered PRD, architecture, K1–K11
Stories, and earlier acceptance contracts remain historical traceability
sources; this website does not replace their source bytes.

> **Implementation snapshot — 2026-09-08.** v0.7 P0–P5 passed local
> acceptance on source `3094b048…`. The artifacts are signed for
> `local-acceptance`, and v0.7 has not been formally released. v0.8 is in
> development with no acceptance directory at this snapshot. See
> [Status and roadmap](../roadmap/) for the full evidence boundary.

## Historical numbered contract

| Area | Requirement IDs | Public contract |
|---|---:|---|
| Product axioms | KFR-001–006 | PostgreSQL-only control plane; AI is an actor; every write has a Plan; no Driver bypass |
| Resource and identity | KFR-010–021 | Durable resources, access-path separation, multi-evidence identity, explicit management state |
| Capability | KFR-030–037 | Intrinsic and effective capability; `unknown` and `insufficient_privilege` remain explicit |
| Connection, discovery, import | KFR-050–060 | Staged probes, partial evidence, candidate graphs, bounded SSH tunnels |
| Plan, Policy, Approval | KFR-070–081 | Immutable plan hash, stale detection, scoped policy, separation of duty |
| Durable Operation | KFR-090–103 | Persistent steps, leases, locks, crash recovery, ordered events, honest ambiguity |
| Drivers and three domains | KFR-120–132 | Typed SPI; Patroni, Pigsty, and SQL share one northbound authority |
| Local and Site Agent | KFR-150–157 | Independent SQLite Store; loopback bootstrap; outbound mTLS typed execution |
| Console and Assistant | KFR-170–180 | Resource-scoped IA, capability-driven actions, constrained Assistant and MCP |
| Auth, secrets, audit, licensing | KFR-190–199 | Scoped authorization, CredentialRef, structured redaction, append-only audit, OSS reliability |
| System qualities | KNR-001–020 | Determinism, bounded inputs, recovery, Store parity, compatibility, evidence governance |
{.wide .expand}

The IDs remain stable traceability keys and the completed evidence remains
auditable. Their original Story-level completion process applies to C0–K11
history. It is not the acceptance workflow for new v0.7+ work.

## Current Epic exits

| Train | Epic exits | Current state |
|---|---|---|
| v0.7 cockpit | P0 gate cleanup; P1 fleet/timeline; P2 direct DBA; P3 health report; P4 protection; P5 Pigsty read view | All six locally accepted; formal release pending |
| v0.8 reversible gates | P6 policy and temporary access; P7 cluster governance; P8 Patroni UI; P9 alert inbox; P10 operability | In development; none accepted in this snapshot |
| v0.9 Pigsty depth | P11 inventory editor; P12 SOP library; P13 job recovery drills | Planned |
| v1.0 agent and automation | P14 Site Agent dispatch; P15 junior-DBA account and generated clients | Planned |
{.wide .expand}

An Epic closes only after its real-target journey works and `make test` and
`make lint` pass. Tests follow the working journey and cover its behavior and
kernel invariants; added test lines stay at or below one third of added product
lines. The full `make check-contract` runs once for a release.

## Fixed product boundaries

- PostgreSQL is the only database domain; Patroni is the only HA family.
- `pigsty.yml` remains the inventory truth when the editor arrives in P11.
- Boar owns glanceable instruments and problem panels. Grafana,
  Alertmanager, and VictoriaLogs own dashboards, alert rules, and log search.
- Managed cloud PostgreSQL is covered through the direct PostgreSQL model; it
  is not a separate provider promise.
- Every write still crosses Plan, Policy, Operation, Driver, and Audit. UNKNOWN
  is not collapsed, ambiguous writes are not automatically retried, and AI
  has no approval authority.

See [Contracts and evidence](../contracts/) for change control and
[DN-015](/blog/design/contract-decision-map/) for the decision history.
