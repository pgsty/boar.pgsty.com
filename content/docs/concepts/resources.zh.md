---
title: 资源与身份
description: 在不混淆访问路径、身份事实和字段所有权的前提下建模受管对象。
weight: 10
---

Resource 是 Boar 对可观察或可管理对象使用的版本化 Envelope，承载 Kind、稳定身份、
期望与观测事实、Provenance、Management State、Relationship 与 Field Ownership。

## 当前资源类型

当前 `resource/v1` Registry 包含 Workspace、Fleet、Site、Node、Service、Connection、
CredentialRef、PostgreSQLCluster、PostgreSQLInstance、Endpoint、Database、Role、
Extension、BackupRepository 与 Backup。Plan 和 Operation 引用 Resource，但属于独立的
Kernel Record。Patroni 与 Pigsty 通过这些 Resource、Relationship、Provenance 与 Driver
Evidence 表达，不靠放宽一个通用 Provider Object。Schema 均有版本；增加新 Kind 不会
放宽既有 Kind 的 Decoder。

## Connection 不是身份

Connection URL、Service Entry、Tunnel 或 Site Agent Path 都只是 *Access Path*。多条路径
可以到达同一资产，同一条路径以后也可能指向另一个 Endpoint。因此 Boar 把 Connection
与 PostgreSQL Instance、Asset Identity 分开建模。

同理，PostgreSQL System Identifier 是很强的集群血统证据，但不能单独证明物理实例身份。

## 四条独立轴

不能把以下字段压缩成一个 Provider 标签：

| 轴 | 回答的问题 |
|---|---|
| Provenance | 这个对象或事实从哪里来？ |
| Management Mode | Boar 正在观察、纳管还是主动管理？ |
| Source of Truth | 谁拥有声明事实的权威？ |
| Managed Fields | 每个字段由哪个 Actor 持有？ |

因此，一个对象可以来自 Pigsty Discovery，通过 Direct Connection 观测，同时只由 Boar
管理部分字段。

这已经体现在 v0.7 验收旅程中：尚未 Import 为 Resource 的 Inventory Member 即使相关
Lifecycle Job 成功也保持 UNKNOWN；已授权 Direct Observation 可以与 Pigsty Desired
State 比较，但不会因此转移 Field Ownership。

## Candidate Graph 与纳管

Import 首先生成 Candidate Graph。Identity Matcher 在对象成为 Managed 之前，对证据与
冲突进行分类。Adoption 是显式 Plan；`Stop Managing`、`Delete Resource` 和
`Destroy Target` 是三种副作用完全不同的动作。

## Unknown 也是信息

发现失败永远不能证明不存在。权限不足导致无法观测的字段应记录为
`unknown/insufficient_privilege`，避免低权限 Discovery 删除或禁用它看不到的事实。

设计理由见 [DN-002：资源身份与纳管](/zh/blog/design/resource-identity-and-adoption/)。
