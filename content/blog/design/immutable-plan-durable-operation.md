---
title: 'DN-004: Immutable plans and durable operations'
description: Separate reviewed intent from execution, then commit before crossing the provider boundary.
date: 2026-08-24
lastmod: 2026-09-08
weight: 40
categories: [Architecture]
tags: [plan, operation, policy, recovery]
series: [Control Plane v2]
---

## Decision

The kernel invariant is that every Boar side effect is preceded by an immutable
Plan. Native v2 Server flows seal `boar.pgsty.com/plan/v1`, then create or admit
a durable Operation that commits execution ownership before the Driver can call
an external system. Retained v0.2 paths keep their frozen
`control.Plan/v1alpha1` contract; a legacy path that has not been routed through
the Server kernel must not be presented as an `operation/v1` API.

“One-click” does not mean “no plan.” It means Policy can automatically admit a
single-step low-risk plan.

## Why Plan and Operation are separate

A Plan is reviewed intent. It can be displayed, compared, approved, rejected,
or allowed to become stale without touching a target. An Operation is a
durable attempt to realize one exact Plan and owns locks, leases, steps, events,
results, and recovery.

Combining them creates two failures: reading a plan can accidentally execute
it, and retrying an execution can silently create a different intent.

## Immutability boundary

The Plan digest covers its complete execution authority: Resource UID,
generation and ETag; Action and ActionVersion; canonical typed Intent and its
schema digest; risk and expiry; CapabilityHash and PolicyHash; preconditions and
warning codes; and each Step's Driver/version, Action/version, target, dependency
set, ArgsDigest, content-addressed PayloadRef, verifier reference/digest, risk,
and reversibility. Executable payload bytes live behind `PayloadRef`; the Plan
seals their reference and digest, not arbitrary embedded commands. Display text
is derived from sealed facts; editing a summary cannot edit the action.

Approval binds the digest. Any relevant change requires a successor Plan and a
new approval.

## Durable-before-call

The worker protocol follows a strict order:

1. atomically persist the Plan, Operation, queued Steps, Resource Lock, and
   initial Event at admission;
2. move the Operation to runnable state and claim a Step with a worker Lease;
3. persist the Step as `RUNNING` with a dispatch commitment;
4. persist `MAYBE_SENT` before any Driver I/O;
5. invoke the typed Driver and obtain its typed Result or enter recovery;
6. stage the Result durably, including SendState, Verification, evidence, and
   any checkpoint;
7. atomically finalize terminal Step/Operation state, Events, Audit, and Lock
   release.

This order closes the “called the provider but crashed before recording it”
window as far as the provider contract permits. When it cannot close the
window, the answer is UNKNOWN—not an invented failure followed by retry.

## Idempotency and locks

Idempotency keys protect admission; they do not make an arbitrary provider
mutation idempotent. Resource locks prevent incompatible Operations. Leases
allow recovery from worker death without granting two workers ownership.

Cancellation is a durable state transition. An HTTP disconnect does not cancel
a confirmed operation, and startup does not blindly replay a pending external
write.

## Historical plans

`plan/v1` is the successor northbound contract to `control.Plan/v1alpha1`,
Legacy Tool Plan, and Pigsty Driver Plan. Migrated flows bridge proven typed
provider plans through adapters or content-addressed payloads instead of
mutating the frozen schemas; the compatibility contracts remain supported.

Operator references: [Plans](/docs/concepts/plans/) and
[Operations](/docs/concepts/operations/).

## Sources

- `BOAR-CHARTER.md` (CKR-001 to CKR-005)
- `control/types.go` and `cmd/boar/cmd/patronictl_runtime.go`
- `plan/types.go`
- `operation/state.go` and `operation/types.go`
- `internal/kernelstore/postgres/operation.go`
- `internal/kernelworker/runner.go`
- `internal/kernelstore/postgres/worker.go`, `internal/kernelstore/postgres/audit.go`, and `internal/kernelstore/postgres/worker_multistep.go`
- `internal/migrate/migrations/0012_kernel_operation_store.sql`
