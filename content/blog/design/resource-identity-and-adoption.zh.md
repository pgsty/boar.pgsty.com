---
title: 'DN-002：资源身份与纳管'
description: 为什么 Connection 不是 Asset，Import 又为什么必须先停在 Candidate Graph。
date: 2026-08-24
lastmod: 2026-09-08
weight: 20
categories: [架构]
tags: [资源, 身份, 发现, 纳管]
series: [Control Plane v2]
---

## 问题

PostgreSQL 管理工具常从 DSN 开始，并悄悄让这个 DSN 变成“数据库”的身份。遇到 Service
Discovery、Failover、Tunnel、Shared Endpoint、Clone 或权限限制时，这种简化立即失效。

Pigsty Inventory 会带来另一种陷阱：因为它包含期望名称与地址，Parse 很容易被误认为
“这些资产确实存在”的证据，甚至被误认为修改它们的权威。

## 决策

Boar 把 Resource Identity 与 Access Path 分开，并让四条管理轴彼此独立：

- Provenance：`manual`、`created`、`discovered` 或 `imported` 来源；
- ManagementMode：`unmanaged`、`observed`、`imported`、`managed` 或
  `fully_managed`；
- SourceOfTruth：谁拥有 Resource 声明状态的权威；
- ManagedFields：由 Manager 与 Operation 记录的有限字段所有权。

Adoption 是一种类型化生命周期意图，可以把符合条件的 Resource 转为 `managed`；它不是
`ManagementMode` 的协议值。

Connection 是 Access Path，不是 PostgreSQL Instance Identity。System Identifier 能证明
Cluster Lineage，却不能单独识别物理实例。

## 基于证据的匹配

Discovery 产生 Observation 与 Identity Evidence。公共身份评估使用四个精确 Decision：
`matched`、`candidate`、`conflict` 与 `insufficient_evidence`。Evidence 记录
`observedAt`、Source、Strength 与哈希摘要，而不保存原始身份材料。低权限扫描可以增加它知道
的事实，但不能删除它无权观察的事实。

这正是 `unknown` 与 `insufficient_privilege` 必须成为两个独立 Capability Support 值的
原因。如果把“未观察到”翻译为“不存在”，每个受限连接都可能制造虚假 Drift 或危险
Cleanup。

## Candidate Graph

Pigsty Import 的当前流程是 Analyze → Candidate Graph → Match/Probe → Reviewed Diff →
Plan/Commit。Local Bundle Import 则单独把 Bundle 分析为 Candidate Graph，要求经过认证的
Review，再以 Medium-risk 类型化 Metadata Plan 应用。Credential Material 会被省略；导入的
Resource 在重新绑定 Credential 并完成 Fresh Probe 前保持 Inert，Capability 由目标端重算，
不信任源 Snapshot。Parse 不修改 Target；未审查 Candidate 也不会成为持久化 Resource。

Adoption 也不同于 Object Creation。一个既有 Patroni Cluster 可以先被发现，再通过只修改
元数据、不写 Target 的 Plan 纳管。当前 Importer 要求可达且显式绑定的 Patroni REST
Member Endpoint，并交叉核对 System Identifier 与 Address Evidence；配置 DCS Reader 时
还会校验 DCS Evidence，但 DCS 校验不是必选项。

## 生命周期动词

模型冻结三个独立 Action：

- **Stop Managing**：移除 Boar 主动管理关系，但保留外部 Target。
- **Delete Resource**：按 Retention Policy 删除控制面 Record。
- **Destroy Target**：产生外部破坏性副作用，携带独立 Risk。

当前 Action-risk Registry 将 `resource.stop_managing` 定为 Low、`resource.delete` 定为 High、
`resource.destroy_target` 定为 Critical。

如果 UI 把三者都标成“删除”，它已经违反合同。

## 结果

Resource 能统一 Direct PostgreSQL、Patroni、Pigsty 与 Site Agent 的事实，而不让任何一个
Provider String 充当资产身份。代价是模型更显式，收益是避免对错误数据库执行不可逆操作。

操作参考：[资源与身份](/zh/docs/concepts/resources/)。

## 依据

- `BOAR-CHARTER.md`（CKR-009、CKR-011）
- `resource/types.go`
- `resource/identity.go`
- `internal/importer/pigsty/analyze.go`
- `internal/localmigration/types.go`
- `internal/localimportkernel/driver.go`
- `internal/importer/patroni/graph.go`、`internal/importer/patroni/observer.go` 与 `internal/importer/patroni/projection.go`
- `plan/risk.go`
