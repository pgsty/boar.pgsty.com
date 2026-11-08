---
title: HTTP API
description: Versioned legacy and kernel HTTP surfaces, with one execution authority.
weight: 20
---

Boar serves JSON APIs under its configured `base_path`. Authentication,
workspace scope, RBAC, policy, and conditional headers are part of the request
contract, not optional UI behavior.

## Frozen v0.2 v1alpha1 control API

The checked-in OpenAPI document describes these stable routes:

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Process and contract health |
| GET | `/api/v1/version` | Build and compatibility versions |
| GET | `/api/v1/contexts` | Configured Patroni contexts |
| GET | `/api/v1/contexts/{context}/clusters` | Fresh cluster observations |
| GET | `/api/v1/contexts/{context}/clusters/{scope}` | Canonical topology |
| GET | `/api/v1/contexts/{context}/clusters/{scope}/config` | Dynamic configuration |
| POST | `/api/v1/contexts/{context}/clusters/{scope}/config/plans` | Deterministic config plan |
| POST | `/api/v1/contexts/{context}/clusters/{scope}/members/{member}/restart/plans` | Deterministic restart plan |
| POST | `/api/v1/plans/{planId}/execute` | Execute a confirmed sealed legacy plan once |
{.wide .expand}

These schemas use `boar.pgsty.com/v1alpha1` and remain permanent regression
contracts. Legacy `/api` routes are adapters where documented; they are not a
second semantic authority.

## Kernel resource surfaces

The current source additionally exposes authenticated `/api/v1` routes for:

- Resource list, detail, scope, intrinsic capability, and effective capability;
- Console home, fleet resources, connections, changes, Audit, and timeline;
- PostgreSQL overview, activity, configuration, Top SQL, health report, cluster
  protection, and bounded SQL workspace reads;
- direct-connection test, discover, and save;
- Local import analyze and apply;
- Kernel Plan prepare, read, approve, and apply;
- Operation detail and cancel;
- Site Agent enrollment plans;
- Pigsty inventory, sources, hosts, instances, state, plans, and runs.

The active development tree also contains environment-policy,
PostgreSQL-governance, temporary-access, and maintenance-window routes for the
v0.8 train. Their presence in source is not acceptance evidence for P6-P10.

### v0.7 read-side route highlights

| Method | Route | Surface |
|---|---|---|
| GET | `/api/v1/console/home` | Fleet summary and server-owned thresholds |
| GET | `/api/v1/console/timeline` | Unified timeline |
| GET | `/api/v1/console/resources/{uid}/protection` | Cluster protection view |
| GET | `/api/v1/resources/{id}/postgres/overview` | PostgreSQL overview |
| GET | `/api/v1/resources/{id}/postgres/activity` | Current activity and blocking data |
| GET | `/api/v1/resources/{id}/postgres/configuration` | Configuration and comparison facts |
| GET | `/api/v1/resources/{id}/postgres/top-sql` | Bounded Top SQL view |
| GET | `/api/v1/resources/{id}/postgres/health-report` | Health check report |
| GET | `/api/v1/resources/{id}/postgres/cluster-topology` | Cluster topology |
| GET | `/api/v1/resources/{id}/postgres/recovery-window` | Proven recovery window |
| GET | `/api/v1/resources/{id}/postgres/cluster-metrics` | Cluster metric panel data |
| GET | `/api/v1/resources/{id}/postgres/tree` | SQL workspace object tree |
| POST | `/api/v1/resources/{id}/postgres/query` | Bounded read-only SQL workspace query |
| GET | `/api/v1/resources/{id}/postgres/query-history` | Actor-scoped query history |
{.wide .expand}

The listed surfaces back the unified Console. The
checked-in v0.2 OpenAPI file does not document all successor routes and is not
evidence that every successor route has been promoted to a stable public API.

## Assistant and MCP boundary

`GET /api/v1/mcp/tools` exposes exactly eight model-callable tools:
`resources.list`, `resources.get`, `topology.get`, `metrics.query`,
`logs.query`, `diagnose`, `plan.create`, and `plan.explain`. They can read,
diagnose, create an immutable Plan, or explain one; they cannot approve or
apply it.

The Assistant facade additionally describes `plan.request_approval` and
`plan.apply_approved`, both with `modelCallable=false`. Those controlled
facade actions do not expand the MCP model's authority.

## Mutation protocol

For new APIs, mutation admission uses typed request bodies, workspace and
resource scope, `Idempotency-Key`, and conditional version semantics where
defined. Approval binds the returned plan digest. The client follows the
Operation and its ordered events rather than inferring success from a request
disconnect.

## Errors

Errors are structured as `Code`, `Message`, `Detail`, and `Hint`, with codes of
the form `BOAR-{MODULE}-{NNN}`. See [errors and outcome semantics](../errors/).

Source authority: [`api/openapi.yaml`](https://github.com/pgsty/boar/blob/3671d4caa2f0a91c610f37b0e6c31d1e6159acef/api/openapi.yaml)
for the frozen surface and versioned JSON Schemas under `schema/` for successor
contracts.
