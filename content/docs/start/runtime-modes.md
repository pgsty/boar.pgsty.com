---
title: Runtime modes
description: Choose Server, Local, and Site Agent by state ownership and failure domain.
weight: 30
---

Boar uses one Go source tree and distribution line, but its runtimes occupy
different failure domains.

| Mode | Durable kernel store | Intended use | Network boundary |
|---|---|---|---|
| Server | PostgreSQL metadata database | Shared control plane and Console | Inbound HTTP; provider access from the server or an agent |
| Local | Independent SQLite database | Single-user workstation or contained appliance | Loopback HTTP only |
| Site Agent | Local identity and execution journal | Controlled execution inside a remote site | Outbound mTLS to Server |
{.wide .expand}

## Server mode

`boar server` owns shared Resources, Plans, Operations, approvals, and Audit in
PostgreSQL. The legacy bare `boar` invocation remains a compatibility adapter,
not a second runtime implementation.

Use Server mode when multiple principals, a shared Console, remote sites, or a
central audit authority are required.

## Local mode

`boar local` is a real control plane, not an in-memory demo. It implements the
same minimal kernel store contract over SQLite and serves the embedded UI on
an exact loopback address. Local bootstrapping is single-user and deliberately
refuses remote bind.

Local mode does not require Pigsty lifecycle support to be useful: direct
PostgreSQL discovery and safe control are its first-class journey.

## Site Agent

The Site Agent is an execution channel, not the AI Assistant. The current CLI
implements private initialization, one-shot approved enrollment, mTLS identity
verification, and safe journal inspection. Today, `boar agent run` means
“enroll once if needed, then identify with mTLS”; it is not yet the durable
remote dispatch loop planned for v1.0/P14.

The target design accepts only typed allowlisted actions and preserves an
execution journal across network partitions.

It does not expose `exec(command string)` and it does not become an independent
planner. The Server owns Resource, Capability, Plan, Policy, Operation, and
Audit authority.

## Assistant

The Assistant is an actor inside the Console feature. It may read, explain,
diagnose, and request plans according to explicit `ai.*` capabilities. It does
not receive raw shell, raw SQL write, approval, or force authority.

See the [runtime isolation design note](/blog/design/runtime-modes-and-site-agent/).
