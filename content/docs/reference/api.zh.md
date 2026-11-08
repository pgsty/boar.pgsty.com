---
title: HTTP API
description: 版本化 Legacy 与 Kernel HTTP Surface，共享唯一执行权威。
weight: 20
---

Boar 在配置的 `base_path` 下提供 JSON API。Authentication、Workspace Scope、RBAC、
Policy 与 Conditional Header 都是请求合同的一部分，不是可选 UI 行为。

## 冻结的 v0.2 v1alpha1 Control API

仓库 OpenAPI 文档描述以下稳定 Route：

| 方法 | 路由 | 用途 |
|---|---|---|
| GET | `/api/v1/health` | 进程与合同健康 |
| GET | `/api/v1/version` | Build 与兼容版本 |
| GET | `/api/v1/contexts` | 已配置 Patroni Context |
| GET | `/api/v1/contexts/{context}/clusters` | 新鲜 Cluster Observation |
| GET | `/api/v1/contexts/{context}/clusters/{scope}` | 规范 Topology |
| GET | `/api/v1/contexts/{context}/clusters/{scope}/config` | Dynamic Configuration |
| POST | `/api/v1/contexts/{context}/clusters/{scope}/config/plans` | 确定性 Config Plan |
| POST | `/api/v1/contexts/{context}/clusters/{scope}/members/{member}/restart/plans` | 确定性 Restart Plan |
| POST | `/api/v1/plans/{planId}/execute` | 恰好一次执行已确认密封 Legacy Plan |
{.wide .expand}

这些 Schema 使用 `boar.pgsty.com/v1alpha1`，永久作为回归合同。已有 `/api` Route 在文档
声明处由 Adapter 支持，但不是第二套语义权威。

## Kernel Resource Surface

当前源码还提供带认证的 `/api/v1` Route，用于：

- Resource List、Detail、Scope、Intrinsic Capability 与 Effective Capability；
- Console Home、舰队 Resource、Connection、Change、Audit 与 Timeline；
- PostgreSQL Overview、Activity、Configuration、Top SQL、Health Report、Cluster
  Protection 与有界 SQL Workspace Read；
- Direct Connection Test、Discover 与 Save；
- Local Import Analyze 与 Apply；
- Kernel Plan Prepare、Read、Approve 与 Apply；
- Operation Detail 与 Cancel；
- Site Agent Enrollment Plan；
- Pigsty Inventory、Source、Host、Instance、State、Plan 与 Run。

当前活跃开发树还包含 v0.8 列车的 Environment Policy、PostgreSQL Governance、
Temporary Access 与 Maintenance Window Route。源码中存在这些 Route，不等于 P6-P10
已经取得验收证据。

### v0.7 读侧 Route 摘要

| 方法 | 路由 | Surface |
|---|---|---|
| GET | `/api/v1/console/home` | 舰队摘要与 Server 持有的阈值 |
| GET | `/api/v1/console/timeline` | 统一 Timeline |
| GET | `/api/v1/console/resources/{uid}/protection` | Cluster Protection View |
| GET | `/api/v1/resources/{id}/postgres/overview` | PostgreSQL Overview |
| GET | `/api/v1/resources/{id}/postgres/activity` | 当前 Activity 与 Blocking Data |
| GET | `/api/v1/resources/{id}/postgres/configuration` | Configuration 与对比事实 |
| GET | `/api/v1/resources/{id}/postgres/top-sql` | 有界 Top SQL View |
| GET | `/api/v1/resources/{id}/postgres/health-report` | Health Check Report |
| GET | `/api/v1/resources/{id}/postgres/cluster-topology` | Cluster Topology |
| GET | `/api/v1/resources/{id}/postgres/recovery-window` | 已证明的 Recovery Window |
| GET | `/api/v1/resources/{id}/postgres/cluster-metrics` | Cluster Metric Panel Data |
| GET | `/api/v1/resources/{id}/postgres/tree` | SQL Workspace Object Tree |
| POST | `/api/v1/resources/{id}/postgres/query` | 有界只读 SQL Workspace Query |
| GET | `/api/v1/resources/{id}/postgres/query-history` | Actor-scoped Query History |
{.wide .expand}

上述 Surface 支撑统一 Console。仓库中的 v0.2 OpenAPI 没有记录
所有继任 Route，也不能作为“所有继任 Route 已晋升为稳定公共 API”的证据。

## Assistant 与 MCP 边界

`GET /api/v1/mcp/tools` 精确暴露八个模型可调用工具：`resources.list`、
`resources.get`、`topology.get`、`metrics.query`、`logs.query`、`diagnose`、
`plan.create` 与 `plan.explain`。它们可以读取、诊断、创建 Immutable Plan 或解释 Plan，
不能批准或应用 Plan。

Assistant Facade 另外描述 `plan.request_approval` 与 `plan.apply_approved`，但两者的
`modelCallable=false`。这些受控 Facade Action 不会扩大 MCP 模型的权限。

## 写入协议

新 API 的 Mutation Admission 使用类型化 Request Body、Workspace/Resource Scope、
`Idempotency-Key` 与合同声明的 Conditional Version。Approval 绑定返回的 Plan Digest。
Client 应跟踪 Operation 及其有序 Event，不能从请求断开推断成功或失败。

## 错误

Error 包含 `Code`、`Message`、`Detail` 与 `Hint`，Code 格式为
`BOAR-{MODULE}-{NNN}`。见[错误与结果语义](../errors/)。

冻结 Surface 的源码权威是
[`api/openapi.yaml`](https://github.com/pgsty/boar/blob/3671d4caa2f0a91c610f37b0e6c31d1e6159acef/api/openapi.yaml)，继任合同以
`schema/` 下的版本化 JSON Schema 为权威。
