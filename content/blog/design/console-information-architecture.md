---
title: 'DN-012: A resource-scoped Console'
description: Migrate the UI incrementally from feature pages to scope, capability, plan, and operation.
date: 2026-08-24
lastmod: 2026-09-08
weight: 120
categories: [Design]
tags: [console, ux, navigation, scope, accessibility]
series: [Control Plane v2]
---

## Context

The v0.2 Console established bilingual routes for Overview, DBA Agent, SQL
Editor, cluster detail, sessions, settings, and compatibility. Its route and
behavior contracts remain regression evidence. Its dark visual theme does not:
the current design replaced it with a light-default system on 2026-09-04.

The control-plane kernel introduces Resources, scopes, capabilities, Plans,
Approvals, Operations, and new runtime modes. Simply adding more provider pages
would recreate the fragmentation the kernel removed.

## Decision

Migrate the Console through compatible routes, not a one-shot rewrite. The
current primary navigation registered by the frontend has eight entries:

```text
Home
Connect
Resources
Timeline
Changes
Observe
Govern
Settings
```

The operator's seven recurring questions remain the organizing model. Connect
is an entry action rather than an eighth question, while the v0.7 P1 journey
gave Timeline its own primary route for fast cross-domain event review. This is
why “seven questions” and “eight navigation entries” are both deliberate.

Pages organize context through Workspace, Fleet, Site, Cluster, Instance, and
Database scope. Provider-specific details become Resource tabs or related
links rather than top-level product silos. Old `/overview`, `/fleet`,
`/operate`, and `/chat/:clusterId` links remain redirects or compatibility
routes.

## Capability-driven actions

Buttons consume Effective Capability and show distinct unsupported, unknown,
denied, stale, locked, and approval-required reasons. They do not infer
authority from provider text.

A Direct-only user with one Connection and one Instance should see a simple
instance home, not empty Fleet machinery. Missing facts are not interpreted as
proven absence merely to simplify the screen.

## Plans and operations

Plan review exposes digest, risk, steps, preconditions, expiry, approval, and
reversibility. Operation views preserve exact identity across reconnect and
scope changes, replay events, and present PARTIAL, UNKNOWN, compensation
failure, current known state, and recovery advice honestly.

## Assistant integration

Existing Chat routes and Block renderers remain compatible while product
language moves toward Assistant. New Plan/Operation blocks use versioned
envelopes. The Assistant cannot gain approval or execution authority through
the UI.

## Implementation status

The former K8 work delivered during the v0.3–v0.6 train is historical
regression evidence. The current tree registers the unified Resources,
Timeline, Changes, Direct DBA, health report, protection, management-adoption,
Pigsty, Observe, and Govern surfaces, backed by `/api/v1/console/*` projections
and typed resource endpoints. The roadmap, rather than the historical K8
story map, is the authority for v0.7–v1.0 scope and acceptance; see
[Status and roadmap](/docs/develop/roadmap/).

ADR-023 also supersedes the older “queries plus deep links” interpretation of
the read side. Boar owns glanceable instruments and problem panels, including
bounded direct collection for targets without the Pigsty monitoring stack: a
10-second collection period, 100-millisecond per-statement limit, and total
budget no longer than one period. Grafana, Alertmanager, and VictoriaLogs still
own dashboard editing, alert rules, and log search; Boar provides context and
deep links to them.

## Accessibility contract

New controls require translated names, keyboard focus behavior, Lucide icons,
CSS-token colors, responsive behavior, and browser evidence. The current theme
is light by default. A `[data-mode="dark"]` token block is reserved, but no
toggle ships yet; dark mode is P10 scope. Scope selection must not clear
unrelated operation state or expose stale authority from another account or
workspace.

## Sources in the current repository

- `docs/design/console-information-design.md` and
  `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.1.0.md`
  — the seven questions and ADR-019 read-model decision.
- `frontend/src/features/controlPlaneShell/PrimaryNavigation.tsx` and
  `frontend/src/App.tsx` — the actual eight-item navigation and current route
  table. Earlier “seven primary destinations” prose is not the current count.
- `frontend/UI_UX_ALIGNMENT.md`, `docs/design/console-overhaul-plan.md`, and
  `frontend/src/styles.css` — current light-default visual contract and
  deferred dark mode.
- `internal/handler/routes.go` and `internal/consoleview/` — current Console
  projection and resource-route implementation.
- `internal/postgresdba/types.go` and
  `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`
  — ADR-023 collection bounds and observability ownership.
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md` — current
  product scope, P1 Timeline, and P10 dark-mode target.
