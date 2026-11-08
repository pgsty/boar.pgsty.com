---
title: Errors and outcome semantics
description: Read structured errors and never collapse an uncertain external write into failure.
weight: 40
---

Boar errors are structured for both humans and automation. For example, the
Operation contract serializes an invalid transition as:

```json
{
  "code": "BOAR-OPERATION-002",
  "message": "illegal Operation transition",
  "detail": "[REDACTED]",
  "hint": "[REDACTED]",
  "path": "$.state"
}
```

Codes follow `BOAR-{MODULE}-{NNN}`. HTTP status is transport information; the
Boar code and typed result remain the semantic contract. The Operation error
codec deliberately redacts `detail` and `hint`; those fields must not be
assumed to contain unfiltered internal diagnostics.

## Three independent result axes

Every write result separates:

| Axis | Exact values | Meaning |
|---|---|---|
| Outcome | `SUCCEEDED`, `FAILED`, `UNKNOWN` | Business result |
| SendState | `NOT_SENT`, `MAYBE_SENT`, `ACCEPTED`, `REJECTED` | Dispatch and provider acceptance evidence |
| Verification | `CONFIRMED`, `UNCONFIRMED` | Whether authoritative evidence resolved the result |
{.wide .expand}

`ACCEPTED` does not prove success, and `CONFIRMED` can accompany a known
failure. There is no `SENT` or `CONTRADICTED` value in these enums.

The canonical uncertain case is:

```text
Outcome=UNKNOWN
SendState=MAYBE_SENT
Verification=UNCONFIRMED
```

It means Boar cannot prove whether the external side effect occurred. It does
not mean “safe to retry.” Inspect provider state and durable Operation/Audit
evidence first.

UNKNOWN can also carry `NOT_SENT / UNCONFIRMED` with
`uncertainty=CONCURRENT_CONFLICT`: a compare-and-set precondition failed and
the earlier observation is no longer authoritative. UNKNOWN is not limited to
transport timeouts. Its terminal Operation record is not reopened for retry.

## Common classes

- `BOAR-AUTH-*`: authentication, session, or token authority.
- `BOAR-RESOURCE-*`, `BOAR-IDENTITY-*`: malformed resources or unresolved identity.
- `BOAR-CAPABILITY-*`, `BOAR-POLICY-*`: unavailable actions or rejected admission.
- `BOAR-PLAN-*`, `BOAR-APPROVAL-*`: invalid, stale, or unauthorized plans and approvals.
- `BOAR-OPERATION-*`, `BOAR-WORKER-*`, `BOAR-STORE-*`: durable execution and integrity.
- `BOAR-CONNECTION-*`, `BOAR-CREDENTIAL-*`, `BOAR-DISCOVERY-*`: access and observation.
- `BOAR-SITEAGENT-*`: enrollment, identity, protocol, or journal failures.

## Client behavior

Clients may retry a read according to its documented semantics. A mutation may
be retried only when its action contract, idempotency key, durable record, and
send state make that safe. A timeout or lost HTTP response alone never grants
permission to replay a write.

See [DN-005: UNKNOWN is a first-class result](/blog/design/unknown-is-a-first-class-result/).

Source: `control/types.go`, `operation/state.go`, and `operation/error.go` in
the Boar source repository.
