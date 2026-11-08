---
title: Plans and policy
description: Bind execution intent into one immutable, reviewable artifact.
weight: 30
---

Every side effect in Boar starts with a Kernel Plan. A “direct” low-risk action
is only a single-step plan that Policy may approve automatically.

The v0.7 acceptance retained the frozen historical Plan schema and added a
separate v0.7 schema profile for new actions; it did not rewrite old Plan bytes,
approvals, or Operations. v0.8 governance source is still under development and
has no completed Epic or train acceptance as of 2026-09-08.

## What a plan binds

A sealed `plan/v1` binds:

- the target Workspace, Resource UID, generation, and etag;
- action, risk, expiry, preconditions, and warning codes;
- typed Intent with its schema version, schema digest, and canonical inputs;
- `capabilityHash` and `policyHash`;
- the step graph, including Driver and Action versions, target, input digest,
  `payloadRef`, verifier reference/digest, risk, and reversibility.

The full hash and Plan ID are derived from the canonical authority fields.
Executable Driver material is referenced through `payloadRef` and bound by
digests, not embedded as arbitrary SQL, argv, or a command string. Requester
and creation time belong to surrounding intake records such as
`internal/nativeplan.Record`; human-readable summaries are projections. They
are not extra fields accepted by the `plan/v1` decoder.

Changing any execution-relevant field produces a different plan hash and
invalidates approval. A driver payload is opaque to casual mutation but remains
validated against the action's closed codec and schema.

## Plan lineages

The repository contains several historical plan types:

| Name | Role |
|---|---|
| Kernel Plan `plan/v1` | Resource-scoped northbound successor contract |
| Patroni Control Plan `control.Plan/v1alpha1` | Frozen, provider-native plan embedded by an adapter |
| Legacy Tool Plan | Console Assistant history, migrating to the kernel exit |
| Pigsty Driver Plan | Source-digest-sealed driver payload |

The successor model preserves proven provider semantics; it does not rewrite a
frozen v1alpha1 schema in place.

## Policy admission

Policy evaluates the immutable plan against the principal, resource scope,
risk, approval state, freshness, capability, and active locks. Admission is a
separate durable decision; creating a plan does not execute it.

For new HTTP APIs, idempotency keys and conditional requests protect admission.
Legacy endpoints receive equivalent protection through adapters.

See [DN-004: Immutable plans and durable operations](/blog/design/immutable-plan-durable-operation/).

Source: `plan/types.go`, `plan/codec.go`, and `internal/nativeplan/types.go` in
the Boar repository.
