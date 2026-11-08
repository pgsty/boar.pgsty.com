---
title: 'DN-015: Control Plane v2 decision map'
description: The original accepted ADR catalog, current amendments, and where each decision is explained.
date: 2026-08-24
lastmod: 2026-09-08
weight: 150
categories: [Architecture]
tags: [adr, decisions, traceability, contract]
series: [Control Plane v2]
---

The frozen Control Plane v2 decision log contains the original 18 accepted
ADRs. Later amendments add decisions without rewriting that history. This map
keeps both layers visible; current delivery scope comes from the product-first
roadmap.

| ADR | Accepted decision | Public explanation |
|---|---|---|
| 001 | Anchor the v0.2 baseline to the reviewed commit; release promotion is separate | [Permanent compatibility](../permanent-compatibility-contract/) |
| 002 | In-repository public packages are the canonical Patroni Driver | [Three domains](../three-domains-one-authority/) |
| 003 | AI actor is Assistant; execution component is Site Agent | [Assistant](../assistant-is-an-actor/), [Runtime modes](../runtime-modes-and-site-agent/) |
| 004 | `plan/v1` is the resource-scoped successor, with typed legacy payloads | [Plans and operations](../immutable-plan-durable-operation/) |
| 005 | Kernel risk is Read/Low/Medium/High/Critical/BreakGlass | [Risk reference](/docs/concepts/risk/) |
| 006 | Operations are execution authority; Jobs remain projections/history | [Plans and operations](../immutable-plan-durable-operation/) |
| 007 | Server uses PostgreSQL Store; Local independently implements SQLite Store | [Runtime modes](../runtime-modes-and-site-agent/) |
| 008 | Durable ordered events are the contract; WS/REST/SSE are adapters | [Operations reference](/docs/concepts/operations/) |
| 009 | Keep Echo, React 19, Router 7, Zustand, React Query, and embedded frontend | [Repository architecture](/docs/develop/repository/) |
| 010 | Tables carry `workspace_id` from day one; first release creates one default Workspace | [Resource identity](../resource-identity-and-adoption/) |
| 011 | Core reliability is OSS; Enterprise gates organizational/compliance complexity | [OSS boundary](../oss-reliability-boundary/) |
| 012 | Keep Assistant/OODA as a feature; move every side effect to Kernel Plan | [Assistant](../assistant-is-an-actor/) |
| 013 | Patroni 4.x, etcd3-only, no Python runtime dependency through v0.5 | [Compatibility](../permanent-compatibility-contract/) |
| 014 | v0.2 SDK, CLI, schemas, APIs, and migrations become permanent gates | [Compatibility](../permanent-compatibility-contract/) |
| 015 | Split research MVP into v0.3/v0.4/v0.5 product proofs | [Kernel](../control-plane-kernel/), [Evidence train](../evidence-driven-release-train/) |
| 016 | Add `server/local/agent/plan/operation`; keep bare server and flat Patroni CLI compatible | [CLI reference](/docs/reference/cli/) |
| 017 | Generalize approval to plan-hash-bound Policy; protect new APIs with idempotency/conditions | [Plans and operations](../immutable-plan-durable-operation/) |
| 018 | SSH Tunnel and backup land in v0.5; restore/PITR in v1; major upgrade/DR in v2 | [Drivers reference](/docs/concepts/drivers/) |
{.wide .expand}

The version schedules in ADR-013, ADR-015, and ADR-018 describe their original
train. The v2.1.0 and v2.2.0 amendments continue the decision sequence:

| ADR | Accepted amendment | Public explanation |
|---|---|---|
| 019 | Add server-side read-only `consoleview` projections; they derive operator answers and never become a new source of truth | [Repository architecture](/docs/develop/repository/) |
| 020 | Add the v0.6 K10/K11 train through additive amendments, expanding historical traceability to 134 requirements and 54 Stories | [Contracts and evidence](/docs/develop/contracts/) |
| 021 | Audit the F8 release lifecycle along the first-parent chain while preserving state-edge, manifest, and receipt rules | [Build and test](/docs/develop/testing/) |
| 022 | Build in trust order and accept one operator-visible Epic at a time; test/lint daily, full contract gate once per release | [Status and roadmap](/docs/develop/roadmap/) |
| 023 | Boar owns instruments and problem panels, including direct polling and short-retention trends; Grafana, Alertmanager, and VictoriaLogs own dashboards, alert rules, and log search | [Status and roadmap](/docs/develop/roadmap/) |
| 024 | Kernel write channels default to enabled and are protected by environment × risk Policy | [Capabilities](/docs/concepts/capabilities/) |
| 025 | Instruction files are living documents and validation code has an explicit budget | [Build and test](/docs/develop/testing/) |
{.wide .expand}

ADR-023 deliberately widens the older “query keys plus deep links” boundary.
For targets without the Pigsty monitoring stack, its direct collector contract
is a 10-second cycle, a 100-millisecond hard timeout per query, and a total
timeout no longer than one cycle. Deep links remain part of the integration
boundary; they are no longer the whole Boar read surface.

The table records accepted decisions, not release promotion. In current source,
the three ADR-024 configuration defaults and `boar.yaml.example` are `true`.
The complete environment-by-risk P6 journey still sits outside the v0.7 local
acceptance record. Likewise, accepted P7–P15 scope is not proof that those Epics
have passed their journeys.

## Change rule

`accepted` means implementation must follow the decision until a successor ADR
or Correct Course amends it. Successors preserve the old text and record the
new scope and impact.

## Normative sources

The Charter owns the product definition and CKRs. The v0.7–v1.0 roadmap owns
current Epics and acceptance; the decision log and its amendments own accepted
architecture decisions. This page is a reader-oriented index, not a
replacement for repository source.

## Sources

- Product definition, CKRs, and frozen source order: `BOAR-CHARTER.md` §§1, 4, 5.
- ADR-001–018: `_bmad-output/planning-artifacts/control-plane-decision-log.md`.
- ADR-019–021: `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.1.0.md`.
- ADR-022–025: `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`.
- Current Epic authority: `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`.
- v0.7 acceptance boundary: `docs/acceptance/v0.7/README.md`.
- Implemented ADR-024 defaults: `internal/config/config.go`, `boar.yaml.example`.
