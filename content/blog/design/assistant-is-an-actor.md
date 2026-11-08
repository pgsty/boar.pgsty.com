---
title: 'DN-008: The Assistant is an actor'
description: Keep AI useful by denying it independent execution and approval authority.
date: 2026-08-24
lastmod: 2026-09-08
weight: 80
categories: [Security]
tags: [assistant, ai, mcp, tools, prompt-injection]
series: [Control Plane v2]
---

## Decision

Boar keeps its DiagnosticEngine, Session state machine, FastPath, and
AgentBridge as a Console Assistant feature. The Assistant is not the system
core. Every side effect it proposes exits through the same Kernel Plan used by
humans, API clients, CLI, and MCP.

## Authority model

The Charter defines the following capability vocabulary, including future
levels; this is not a list of currently model-callable tools:

```text
ai.read
ai.explain
ai.diagnose
ai.plan
ai.request_approval
ai.apply_approved
ai.auto_remediate_low
```

They are not L1–L5 safety levels and do not imply human roles. In particular,
the Assistant has no raw shell, raw SQL write, approve, force, or arbitrary
tool-registration authority.

The AI Principal and Approver Principal are separate. The controlled Assistant
facade can request review and apply an already-approved exact plan hash, but
both descriptors currently have `modelCallable=false`. The model cannot invoke
them. `ai.auto_remediate_low` is absent from the current inventory. No Assistant
can approve its own plan or edit the plan after approval.

## Untrusted inputs

Database comments, SQL, logs, inventory, README files, alerts, provider error
messages, and retrieved documentation are all untrusted data. They may contain
instructions intended to influence the model.

Closed-schema tools make those instructions data rather than authority. Tool
selection is limited by Effective Capability, and arguments pass typed
validation. Human/service approval verifies principal identity and plan hash;
it never trusts model prose as authorization.

## MCP boundary

The current MCP inventory exposes exactly eight model-callable tools:
`resources.list`, `resources.get`, `topology.get`, `metrics.query`,
`logs.query`, `diagnose`, `plan.create`, and `plan.explain`. It exposes no raw
write, approval, force, or Apply tool.

The wider authenticated Assistant facade also describes
`plan.request_approval` and `plan.apply_approved`, but both are
`modelCallable=false`. Requesting review records no approval decision; Apply
accepts only an already-approved exact immutable Plan hash and delegates to the
Kernel path. P10 plans to add these two governed operations to MCP without
giving the model approval authority. A generic execution tool would still
violate the product contract.

## Existing user value

Re-centering the product does not delete the Assistant. Existing sessions,
seven Block renderers, versioned WebSocket envelope, replay, diagnostic cards,
and graceful LLM degradation remain. The change is ownership: Assistant output
can inform intent, but only the kernel owns mutation.

## Why this is more AI-native

An AI-native system is not one where the model has the most privileges. It is
one where every model contribution is typed, attributable, reviewable,
recoverable, and interchangeable with other actors. By keeping authority
outside model text, Boar can improve or replace the model without changing the
control-plane safety contract.

## Sources in the current repository

- `BOAR-CHARTER.md` — product identity, CKR authority boundaries, and the
  `ai.*` capability vocabulary.
- `internal/assistantmcp/contracts.go` and
  `schema/assistantmcp/v1/inventory.schema.json` — exact Assistant/MCP
  inventories, closed argument schemas, and `modelCallable` values.
- `internal/server/assistant_mcp.go` and `internal/handler/routes.go` — the
  authenticated facade and its Kernel delegation.
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md` — P10
  scope for the two future MCP operations.
