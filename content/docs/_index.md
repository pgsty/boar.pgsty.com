---
title: Boar Documentation
linkTitle: Docs
description: Operate PostgreSQL through one explicit, auditable control-plane model.
search_keywords: [Boar, PostgreSQL control plane, Pigsty, Patroni, operations]
type: docs
icon: fa-solid fa-book
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
outputs: [HTML, RSS, markdown, LLMSFULL]
cascade:
  type: docs
  theme_color: '#245f94'
  theme_color_dark: '#68a9df'
  navbar_autohide: false
  footer_style: slim
  search_boost: 1.35
---

Boar is Pigsty's PostgreSQL control plane. It brings direct PostgreSQL access,
Patroni HA management, and Pigsty lifecycle operations under one Resource,
Capability, immutable Plan, durable Operation, and Audit model.

> [!IMPORTANT]
> This site preserves the historically accepted Fusion `v0.2` contracts and
> documents the current product-first train. The v0.7 cockpit passed local
> acceptance on source `3094b048…`, but has not been formally released. See
> [Status and roadmap](develop/roadmap/) for the exact evidence boundary.

## Choose your path

- [Get started](start/) — install Boar, run the local or server control plane, and learn the safe first workflow.
- [Core concepts](concepts/) — understand resources, identity, capability, plans, operations, and risk.
- [Manage PostgreSQL](manage/) — work with direct connections, Patroni, Pigsty, Local mode, and Site Agent.
- [Reference](reference/) — look up the CLI, HTTP API, configuration, errors, and compatibility contracts.
- [Administration](admin/) — secure, upgrade, recover, audit, and operate Boar.
- [Development](develop/) — check current status, follow the roadmap, build the repository, and understand its gates.
  {.cards}

## Product boundary

The Assistant, Console, CLI, API, MCP, and Site Agent are actors or entry
points. None of them is allowed to bypass the kernel. The shortest legitimate
write path is still:

```text
Resource → Capability → Plan → Policy → Operation → Driver → Audit
```

If you are evaluating Boar's architecture rather than operating it, start with
the [control-plane kernel design note](/blog/design/control-plane-kernel/).
