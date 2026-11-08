---
title: 'DN-003: Capability, not provider flags'
description: Why action availability must be evaluated, explainable, and shared by every entry point.
date: 2026-08-24
lastmod: 2026-09-08
weight: 30
categories: [Architecture]
tags: [capability, policy, ux, authorization]
series: [Control Plane v2]
---

## Problem

Provider-driven interfaces tend to hard-code logic such as “show Failover when
provider is Patroni” or “show Backup when this came from Pigsty.” Those checks
mix product taxonomy, target support, transport availability, credentials,
permissions, current state, and policy into one brittle condition.

The same action then behaves differently in CLI, Console, API, and Assistant.
Worse, a hidden button gives the operator no reason.

## Decision

Boar models two layers:

- **Intrinsic Capability**: what the Resource and typed Driver can support in
  principle.
- **Effective Capability**: whether this principal may perform this action on
  this Resource now, with explicit reason codes.

Intrinsic evaluators consume typed observations such as provider, interface,
version, topology, current state, and prerequisite facts. A separate scoped
Policy projection applies principal and Resource scope, channel, risk, approval,
MFA, maintenance-window, and lock requirements. Individual actions can add
typed relationship, connection, credential, identity, and freshness
prerequisites; those inputs are not inferred from a provider name.

At the wire boundary, `support` is one of `supported`, `unsupported`, `unknown`,
or `insufficient_privilege`. `intrinsic` and `effective` are nullable booleans,
so an unknown conclusion remains distinct from `false`. A missing privilege
probe cannot become either a grant or a denial without evidence.

## Capability is not execution

An effective capability that says “available” means the action may proceed to
planning. It does not authorize an unplanned provider call. The resulting Plan
still binds exact input, risk, preconditions, policy, and target version.

Conversely, “unavailable” is a structured result, not a disabled CSS class.
Examples include:

- missing, stale, or insufficient-privilege observation facts;
- no verified Connection or usable credential;
- topology or provider version outside the supported boundary;
- an inactive principal or insufficient Resource scope;
- Policy denial by action, risk, environment, or channel;
- required confirmation, approval, Resource Lock, maintenance window, or MFA.

## One answer across surfaces

The Server Resource API currently returns intrinsic snapshots and a separate
Policy-aware effective projection, and the Console renders that authority.
The retained Patroni-compatible CLI still has its public `control.Service` and
local evaluation boundary. MCP apply coverage is scheduled in the v0.8 P10
roadmap rather than complete today. The invariant is that these surfaces must
converge on the same Resource, Capability, Plan, Policy, and Audit semantics;
it is not a claim that every client already consumes the Resource API endpoint.

This also simplifies extensibility: a new Driver contributes typed actions and
facts to the evaluator instead of teaching every UI surface a new provider
name.

## Risk remains kernel-owned

A Driver can declare that it supports an action, but cannot lower the action's
kernel risk. When a legacy provider declaration disagrees with the action-risk
registry, the stricter classification wins.

Operator reference: [Capabilities](/docs/concepts/capabilities/).

## Sources

- `BOAR-CHARTER.md` (CKR-010)
- `capability/types.go`
- `internal/capabilityengine/evaluate.go`
- `internal/scopedpolicy/capability.go`
- `internal/resourceapi/types.go`
- `cmd/boar/cmd/patronictl_runtime.go`
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md` (P10)
