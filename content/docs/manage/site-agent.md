---
title: Site Agent
description: Establish an outbound mTLS site identity within the current prototype boundary.
weight: 50
---

The Site Agent is the name reserved for Boar's controlled remote execution
component. It is distinct from the AI Assistant and from the control-plane
Server.

> [!NOTE]
> Status on 2026-09-08: the repository contains the K7 enrollment, mTLS,
> journal, typed-action, and partition-safety prototype contracts. The current
> `boar agent run` lifecycle only enrolls when needed and then performs bounded
> read-only identity checks. It is not a general worker or Plan dispatch loop.
> Making Site Agent a Plan dispatch channel is v1.0 P14 work and has not passed
> Epic or train acceptance.

## Lifecycle

```text
init → approved enrollment → persisted identity → repeated mTLS identify
```

The current CLI exposes:

```text
boar agent init
boar agent enroll
boar agent identify
boar agent run
boar agent journal
```

Use an explicit owner-private Agent configuration. Bootstrap enrollment is a
one-time authority and is not automatically retried after an ambiguous
attempt.

`agent run` enrolls at most once when no identity exists, reports the identity,
and repeats `identify` at the configured interval. Authentication or transport
failure exits. It binds no listening socket and reports
`executionAvailable: false` in the current runtime.

## Trust and transport

The agent initiates the connection outbound. Enrollment converts an approved
bootstrap into a persistent mTLS identity; subsequent sessions prove that
identity rather than resending bootstrap material.

Certificates, private keys, and journal state remain owner-private. The Server
binds the agent identity to workspace, site, capabilities, and action scope.

## Typed-action boundary

The prototype protocol and journal define versioned action names, closed
payloads, local allowlists, and recovery evidence. They never accept
`exec(command string)`. Shell, SQL, and Ansible details may exist only inside
reviewed typed action implementations. These contracts constrain future P14
dispatch; they do not mean the current `agent run` polls for or executes work.

## Execution journal

The execution-journal prototype records receipt, commitment, send state,
result, and verification needed to reconcile a network partition. The current
CLI can inspect one exact safe record with `agent journal --request-id`; it does
not create a general dispatch loop. Server Operation and Agent journal remain
separate evidence authorities so a disconnect cannot fabricate success or
justify a second execution.

See [DN-007: Runtime modes and Site Agent](/blog/design/runtime-modes-and-site-agent/).
