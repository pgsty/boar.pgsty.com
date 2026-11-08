---
title: Patroni HA
description: Manage Patroni through the native Boar SDK and the shared kernel.
weight: 20
---

Boar's Patroni driver is built on the repository's public Go packages rather
than a Python subprocess or an external replacement. This preserves the
validated REST, etcd, PostgreSQL, planning, verification, and failure
semantics of the v0.2 baseline.

> [!NOTE]
> Status on 2026-09-08: v0.7 locally accepted the read-side cluster protection
> view against real Patroni targets. First-class Console actions and
> postcondition journeys belong to v0.8 P8, which has not passed Epic or train
> acceptance.

## Supported boundary

- Patroni `>=4.0.0,<5.0.0`; reviewed release `4.0.7` and source lane `4.1.0`.
- etcd3 DCS only for the current compatibility window.
- No runtime dependency on Python or `patronictl`.
- Native Cobra commands preserve human, JSON, and YAML contracts.

Other versions are unverified, not implicitly supported.

## Nineteen compatible commands

The current CLI exposes:

```text
list      topology  history  show-config  edit-config  version
pause     resume    restart  reload       reinit       switchover
failover  flush     remove   dsn          query        promote-cluster
demote-cluster
```

Use `boar <command> --help` for exact flags. These commands remain flat for
script compatibility; they are not moved under a new namespace. Boar also
provides `discover`, which is an additional Boar command and is not one of the
19 patronictl-compatible commands.

## Kernel migration

Existing `control.Plan/v1alpha1` remains the typed Patroni plan. The adapter
embeds it as a driver payload inside a resource-scoped Kernel Plan. K2 proved a
restart vertical slice across crash windows; K5 migrated the Patroni domain to
one dispatch authority while retaining 19-command differential parity.

Legacy routes may project the Operation into an old Console Job, but only the
kernel lane may call Patroni.

Server mode defaults both `kernel_patroni_restart` and
`kernel_patroni_domain` to `true`. These switches do not authorize an action:
Effective Capability, environment policy, exact Plan admission, approval when
required, resource locks, and Audit remain mandatory. In a Kernel-enabled
deployment, mutating flat compatibility commands refuse standalone execution
and require exact Server Kernel Plan approval and admission.

## Accepted protection view

The v0.7 view combines topology, replication, routing evidence, cluster
instruments, and pgBackRest archive evidence. Pigsty targets may use
VictoriaMetrics; a target without a monitoring profile uses the bounded Direct
collector. Missing VIP, HAProxy, PgBouncer, backup, or metrics channels remain
missing or UNKNOWN rather than becoming healthy zeroes.

The displayed recoverable interval is derived from a proven archive chain. It
is not proof that an actual restore or PITR drill succeeded; those journeys are
scheduled for v0.9 P12-P13.

## Safety highlights

- Switchover is High; failover is Critical in the kernel registry.
- Reload is Low, restart is Medium, and reinitialize is High.
- DCS fallback and REST transport evidence remain distinct.
- Outcome, send state, and verification are recorded independently.
- An ambiguous Patroni write becomes UNKNOWN and is not automatically retried.
- Edit-config is at least High and may rise to Critical according to affected fields.

For the design rationale, see [DN-006](/blog/design/three-domains-one-authority/)
and [DN-010](/blog/design/permanent-compatibility-contract/).
