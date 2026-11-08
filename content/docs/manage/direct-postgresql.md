---
title: Direct PostgreSQL
description: Discover an arbitrary PostgreSQL URL and expose only evidence-backed actions.
weight: 10
---

> [!NOTE]
> Status on 2026-09-08: the v0.7 P2 real-target journey passed local
> acceptance. It covered local PostgreSQL and a separate RDS-like PostgreSQL
> target; it did not use a cloud-vendor RDS account. v0.7 has not been
> officially released.

Direct mode starts from an access path and builds a resource graph. It does not
turn a DSN into an unquestioned asset identity.

## Journey

1. Create a Connection with a URL and a CredentialRef.
2. Probe transport and authentication without publishing secret material.
3. Discover PostgreSQL identity, version, role, databases, settings, and
   relationships according to the principal's privileges.
4. Match the observation to an existing asset or propose a new one.
5. Evaluate intrinsic and effective capabilities.
6. Expose read surfaces immediately; require a Plan for every write.

Connection and credential records are separate. Durable rows contain encrypted
credential envelopes or SecretRefs with metadata and key version; Resources,
Plans, Events, and Audit never contain plaintext credentials.

## Accepted DBA surfaces

The accepted Server journey covers overview instruments, activity and a lock
wait tree, configuration comparison, Top SQL when `pg_stat_statements` is
available, privileged server-log reading, an object tree, a conservative SQL
workspace with EXPLAIN, encrypted per-user query history, and pgAdmin
`servers.json` import. Collection uses a 10-second cycle, a 100-millisecond
hard timeout per target query, and short-retention samples.

A low-privilege connection remains useful: fields it cannot inspect are
UNKNOWN with a reason rather than fabricated empty data. The SQL workspace is
a bounded read tool, not a complete pgAdmin replacement and not an arbitrary
SQL-write authority.

## Session actions and the next governance train

The v0.7 journey proved session cancellation through a reviewed immutable Plan,
Policy attestation, durable Operation, verification, and Audit. The registry
classifies session cancel as Low and session terminate as Medium. Availability
still comes from Effective Capability; a visible action is not execution
authority by itself.

The earlier K5 typed-write foundation remains implemented: it includes
create-index and parameter-change Plans, with parameter changes classified as
dynamic, reload, or restart work. v0.8 adds the product-facing cluster
governance and unified approval journeys for parameters, databases, roles,
extensions, HBA reconciliation, and temporary access. That v0.8 source is
still work in progress and has not passed Epic or train acceptance.

`kernel_postgres_write` defaults to `true` in Server mode, but the flag only
makes the lane available for evaluation: Capability, Policy, exact Plan
admission, locks, and Audit still apply. Arbitrary SQL write is not a
northbound capability, and lost acknowledgement cannot trigger a blind replay.

## Health and cost evidence

The accepted v0.7 health report checks evidence such as bloat, unused indexes,
missing primary keys, HBA and `trust` exposure, superusers, certificate expiry,
password state, and protective settings. Unsupported or inaccessible checks
remain UNKNOWN. The TCO panel calculates from operator-provided inputs; it does
not fetch cloud prices or exchange rates.

## Transport security

Use `sslmode=verify-full` where possible. Credentials, trust roots, service
files, passfiles, and TLS key files each have explicit source and file-mode
rules. Channel binding `require` must observe `SCRAM-SHA-256-PLUS`; failure is
an authentication error, not a warning.

Read [security](../../admin/security/) and the
[compatibility matrix](../../reference/compatibility/) before production use.
