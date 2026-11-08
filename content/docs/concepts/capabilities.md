---
title: Capabilities
description: Explain what the target supports, what the principal may do, and why.
weight: 20
---

Capability is the contract between discovered facts and available actions. The
Console must not decide whether to show an action by testing a provider string.

## Intrinsic and effective

- **Intrinsic capability** describes what the resource and driver can do in
  principle: for example, a Patroni cluster supports switchover, or a
  PostgreSQL target exposes dynamic parameter metadata.
- **Effective capability** is the result after access reachability,
  credentials, resource state, policy, risk, license boundary, principal
  scope, and freshness are considered.

The effective record contains an explicit decision and reasons. A disabled
button is insufficient; the operator needs to know whether the blocker is a
missing credential, stale discovery, insufficient privilege, a resource lock,
or an approval requirement.

Feature-lane configuration is only one input. In Server mode the three Kernel
write lanes currently default to enabled, but an action is usable only when its
Effective Capability is affirmative after Policy and current evidence are
applied. A feature flag never grants a principal authority.

## Evaluation inputs

```text
resource facts
+ relationship context
+ driver declaration
+ connection and credential state
+ principal scope
+ policy and risk
+ freshness and locks
= effective capability with reasons
```

Unknown input is preserved. For example, the absence of a privilege probe
cannot be treated as a positive denial or an affirmative grant.

## Stable action identity

Capabilities refer to versioned action identities, not arbitrary commands.
The action registry binds each action to typed input, risk classification,
driver support, and verification behavior. A driver cannot advertise a lower
risk than the kernel registry.

## User-interface rule

Every entry point—API, CLI, Console, MCP, or Assistant—must use the same
effective capability decision. UI presentation may differ, but authority may
not.

The v0.7 journeys locally accepted read-side capability reasons and the Low
session-cancel path. Capabilities appearing in in-progress v0.8 source are not
accepted product claims until their Epic and train journeys pass.

See [DN-003: Capability, not provider flags](/blog/design/capability-not-provider-flags/).
