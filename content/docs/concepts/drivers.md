---
title: Drivers
description: Keep provider semantics typed and bounded beneath the kernel.
weight: 60
---

A Driver translates a versioned kernel action into provider-specific work. It
is not an alternate execution authority.

## Driver contract

Each action has a closed identity and typed payload. A driver declares support,
validates the payload, prepares the call, reports send state, verifies the
postcondition, and returns structured evidence. It cannot bypass Planner,
Policy, Operation, or Audit.

The kernel persists the step commitment before invoking the driver. The driver
does not decide whether the caller is authorized and does not write an
independent audit history.

## First domains

- **Patroni Driver** builds on the repository's public `patroni`, `dcs`,
  `dcs/etcd3`, `postgres`, and `control` packages. It preserves 19/19 native
  CLI parity and frozen failure semantics.
- **PostgreSQL Driver** discovers arbitrary connections and exposes typed read
  actions. Its earlier K5 typed-write foundation includes create-index and
  parameter-change Plans; session cancel was accepted in the v0.7 product
  journey. v0.8 adds cluster governance and unified approval UX, and remains
  under development without Epic or train acceptance. Raw SQL write is not a
  northbound action.
- **Pigsty Driver** retains source digest, redaction, argv/environment
  allowlists, and postcondition verification. It never accepts arbitrary
  Ansible or shell from the GUI.
- **Site Agent prototype** proves enrollment, outbound mTLS identity, typed
  protocol boundaries, and journal semantics. The current `agent run` performs
  identity checks rather than polling or executing Plan work.

Backup, package/repository, observe, and SSH-tunnel provider contracts were
built in the earlier K9 line. The current product train accepts user-visible
journeys separately: v0.7 covers read-side instruments and evidence, v0.8
covers reversible governance, v0.9 P12-P13 covers PITR templates and real
restore drills, and v1.0 P14 turns Site Agent into a general Plan dispatch
channel. Source presence alone does not mark one of those journeys accepted.

## One dispatch authority

During migration, legacy endpoints may remain, but a domain has exactly one
side-effect dispatch lane. An adapter may project a kernel operation back into
a legacy Job; it may not cause a second provider call.

See [DN-006: Three domains, one dispatch authority](/blog/design/three-domains-one-authority/).
