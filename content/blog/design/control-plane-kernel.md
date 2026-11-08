---
title: 'DN-001: The control-plane kernel'
description: Why Boar is a PostgreSQL control plane first, and an AI product second.
date: 2026-08-24
lastmod: 2026-09-08
weight: 10
categories: [Architecture]
tags: [kernel, control-plane, charter, product]
series: [Control Plane v2]
---

## Decision

Boar's first product identity is the PostgreSQL control plane for Pigsty. It
unifies direct PostgreSQL management, Patroni HA adoption, and Pigsty lifecycle
operations through one Resource, Capability, immutable Plan, durable Operation,
and Audit kernel.

The AI Assistant is an Actor. The Web Console, CLI, API, MCP, and Site Agent are
entry points or execution channels. None of them is the control plane itself,
and none may bypass the kernel. This is the normative architecture invariant;
it does not imply that every retained v0.2 path already calls the same HTTP
service internally.

## Why the re-charter was necessary

The v0.2 Fusion baseline proved valuable pieces: a diagnostic Assistant,
native Patroni control, typed PostgreSQL and etcd providers, durable Jobs and
approval, Pigsty integration, and a bilingual Console. But “AI-first DBA agent”
was a poor architectural center. It made Assistant workflows look like the
owner of mutation semantics and left direct, HA, and lifecycle operations as
parallel product lines.

A control plane needs a stable answer to seven questions regardless of who
asks:

1. What is the target Resource?
2. How certain is its identity?
3. What Capability is effective now, and why?
4. What exact change is proposed?
5. Which Policy and approval admit it?
6. What durable Operation owns execution and recovery?
7. What evidence and Audit prove the result?

Moving those questions into the kernel makes Assistant automation safer and
also makes the product useful without an LLM.

## Kernel boundary

```text
Actor / entry point
        │
        ▼
Resource → Capability → Planner → Policy → Operation → Driver
                                                   │
                                                   ▼
                                                Audit
```

Drivers retain provider-native semantics but cannot become alternate planners.
The kernel and public packages do not depend on Console, License, LLM, Web, or
legacy metadata tables.

## Release consequences

The original decision split the research MVP into v0.3–v0.5 product proofs;
v0.6 later completed the world-merge work. Those releases and their K-series
contracts are now historical delivery and regression evidence.

CC-CP-007 changed the schedule and acceptance method without changing this
kernel decision. The current product-first train is v0.7 read-side trust, v0.8
reversible gates, v0.9 destructive Pigsty lifecycle, and v1.0 agent and
automation. See [Status and roadmap](/docs/develop/roadmap/).

## Compatibility

The re-charter is additive. The v0.2 public packages, 19 CLI commands,
v1alpha1 schemas, UNKNOWN semantics, durable confirmation, Pigsty safety, and
release evidence remain permanent regression contracts.

## Sources

- `BOAR-CHARTER.md`
- `_bmad-output/planning-artifacts/control-plane-architecture.md`
- `_bmad-output/planning-artifacts/control-plane-decision-log.md` (ADR-012 and ADR-015)
- `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md` (ADR-022 to ADR-025)
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`

For v0.7 and later scheduling and acceptance, CC-CP-007 and the roadmap above
supersede the older story-level acceptance framework. The readable
documentation starts at [Core concepts](/docs/concepts/).
