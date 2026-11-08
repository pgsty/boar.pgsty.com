---
title: 'DN-005: UNKNOWN is a first-class result'
description: Why uncertainty is preserved across SDK, API, Operation, Audit, and UI.
date: 2026-08-24
lastmod: 2026-09-08
weight: 50
categories: [Reliability]
tags: [unknown, retry, verification, safety]
series: [Control Plane v2]
---

## The dangerous simplification

Distributed writes have an unavoidable case: the client loses its response
after the request might have crossed the boundary. Reporting “failed” feels
convenient, but it invites an automatic retry that can repeat a failover,
restart, DCS deletion, SQL change, or lifecycle action.

Boar refuses that simplification.

## Three axes

Every terminal mutation Result records three independent facts:

- **Outcome**: `SUCCEEDED`, `FAILED`, or `UNKNOWN` business result.
- **SendState**: `NOT_SENT`, `MAYBE_SENT`, `ACCEPTED`, or `REJECTED` transport
  fact. `ACCEPTED` and `REJECTED` are exact transport outcomes, not a generic
  “sent” value.
- **Verification**: `CONFIRMED` or `UNCONFIRMED`. Success versus failure is
  carried by Outcome; Verification has no `CONTRADICTED` wire value.

The canonical ambiguous result is:

```text
UNKNOWN / MAYBE_SENT / UNCONFIRMED
```

It is not a decorated error. It changes allowed recovery behavior.

The truth table also permits `UNKNOWN / ACCEPTED / UNCONFIRMED`, and one narrow
non-transport exception: `UNKNOWN / NOT_SENT / UNCONFIRMED` with
`CONCURRENT_CONFLICT`. These are distinct, validated tuples rather than prose.

## No blind retry

An ambiguous write is never automatically retried. Recovery must use one of:

- a provider-defined idempotency contract;
- direct postcondition verification;
- a durable journal that proves the call was not sent;
- explicit operator reconciliation followed by a new plan.

The retry decision belongs to the typed Action and Operation recovery model,
not to an HTTP client library or generic queue.

## Across the system

UNKNOWN is preserved in public Go types, JSON Schema, API responses, CLI
machine output, Operation Events, Audit, legacy Job projections, and the
Console. A UI that paints it red and labels it “Failed” violates the contract
even if the backend record remains correct.

The same principle applies to discovery: “could not observe” is not “does not
exist.” Unknown is evidence about the limits of evidence.

## Incident behavior

When an Operation is UNKNOWN:

1. the worker performs no automatic replay; operators should also hold
   dependent destructive actions until reconciliation;
2. preserve Plan, Step, Event, driver, and transport evidence;
3. inspect the provider and Site Agent journal where applicable;
4. record reconciliation evidence;
5. create a new Plan only after current state is known well enough.

This may require more operator attention than a binary success/failure model.
That is the honest cost of controlling stateful infrastructure.

Operator reference: [Errors and outcome semantics](/docs/reference/errors/).

## Sources

- `BOAR-CHARTER.md` (CKR-004 and CKR-005)
- `control/types.go`
- `operation/state.go`
- `operation/types.go`
- `internal/kernelworker/recovery.go`
- `internal/kernelworker/runner.go`
