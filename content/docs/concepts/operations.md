---
title: Operations and events
description: Execute a sealed plan with durable state, honest recovery, and replayable evidence.
weight: 40
---

An Operation is the durable execution of one admitted plan. It is not a UI job
and not an in-memory goroutine.

## Authority model

The kernel store owns Operation, Step, Event, approval, lock, lease, and
idempotency state. The worker protocol commits the transition that establishes
execution ownership before calling an external system.

```text
admit plan
  → create operation and initial event
  → acquire resource lock and worker lease
  → durable RUNNING / step commitment
  → typed driver call
  → verification
  → terminal outcome and audit
```

## Crash behavior

Recovery depends on the last durable commitment and provider evidence:

- Before external-call commitment, the step may be safely claimed according to the lease protocol.
- After a provably idempotent call, a replay still requires the action's explicit contract.
- When the call may have been sent and cannot be verified, the result becomes UNKNOWN.
- Ambiguous writes are never retried automatically.

Resource locks prevent incompatible concurrent operations. Cancellation is a
durable request with defined terminal semantics; an HTTP disconnect does not
silently cancel a confirmed operation.

## Events and replay

Operation events are ordered, durable, and replayable. Transport is an adapter:
the current system uses the versioned WebSocket envelope and paged REST replay.
Adding SSE later would not change event authority. Product views may cap one
response and state that it was truncated; the durable event count and terminal
Operation state remain distinct from the displayed slice.

## Jobs are projections

The legacy `jobs` table remains for historical Console and Chat projections.
New `operations`, `operation_steps`, and `operation_events` are execution
authority. Historical job rows are not rewritten into fake operations.

See [DN-004](/blog/design/immutable-plan-durable-operation/) and
[DN-005](/blog/design/unknown-is-a-first-class-result/).
