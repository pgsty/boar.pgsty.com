---
title: Risk and approval
description: Apply one conservative risk scale and bind approvals to exact plans.
weight: 50
---

Kernel risk is action-specific and ordered:

| Risk | Legacy mapping | Representative action |
|---|---|---|
| Read | L1 | topology, logs, metrics |
| Low | L2 | session cancel, reload, metadata adoption |
| Medium | L3 | session terminate, restart, dynamic parameter |
| High | L4 | switchover, reinitialize, add replica |
| Critical | L5 | failover, promote/demote, remove or destroy |
| BreakGlass | none | no action is registered at this level today |

The L1–L5 mapping translates frozen legacy records. It cannot lower the
kernel's action classification. When declarations disagree, Boar uses the more
restrictive risk.

For example, legacy `patroni_failover` was declared L4 in one path, while the
kernel fixes failover at Critical. `patroni_edit_config` is at least High and
may become Critical according to affected fields.

Server mode defaults `kernel_patroni_restart`, `kernel_patroni_domain`, and
`kernel_postgres_write` to `true`. This enables the lanes for Capability and
Policy evaluation; it does not auto-approve their actions or bypass exact Plan
admission.

## Approval binding

An approval binds the full plan hash, the approver principal, scope, policy,
and time. It becomes stale when the plan, action version, target evidence,
expected resource version, or relevant policy state changes.

The legacy two-administrator L5 mechanism becomes one Policy implementation;
approval is no longer a Console-Job-only concept.

## Principal separation

The actor that proposes a plan is not automatically allowed to approve it. In
particular, AI Principal and Approver Principal are separate. The Charter's
Assistant capability vocabulary uses `ai.*`, never the L1–L5 labels.
The current model-callable surface is limited to read, diagnose, and Plan
creation/explanation. `plan.request_approval` and `plan.apply_approved` exist
only in the controlled Assistant facade with `modelCallable=false`.
`ai.auto_remediate_low` is a planned capability, absent from the current tool
inventory. See the [Assistant and MCP API boundary](../../reference/api/#assistant-and-mcp-boundary).

## BreakGlass

BreakGlass is an explicit new category, not “Critical plus one checkbox.” It
requires a distinct policy path, exceptional evidence, and a registered typed
action. The vocabulary exists, but the current action registry assigns no
action to BreakGlass. The normal GUI and Site Agent expose no arbitrary shell.
