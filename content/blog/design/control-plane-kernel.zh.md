---
title: 'DN-001：控制面内核'
description: 为什么 Boar 首先是 PostgreSQL 控制平面，其次才是 AI 产品。
date: 2026-08-24
lastmod: 2026-09-08
weight: 10
categories: [架构]
tags: [内核, 控制平面, charter, 产品]
series: [Control Plane v2]
---

## 决策

Boar 的第一产品身份是 Pigsty 的 PostgreSQL 控制平面：用统一 Resource、Capability、
不可变 Plan、持久化 Operation 与 Audit 内核，归一任意 PostgreSQL 直连、Patroni HA 纳管
与 Pigsty 生命周期运维。

AI Assistant 是 Actor。Web Console、CLI、API、MCP 与 Site Agent 是入口或执行通道，
它们都不是控制面本体，也不能绕过内核。这是规范架构的不变量，并不表示所有保留的
v0.2 路径在内部都已经改为调用同一个 HTTP 服务。

## 为什么必须重新立项

v0.2 Fusion 基线已经证明了许多有价值的部件：Diagnostic Assistant、原生 Patroni Control、
类型化 PostgreSQL/etcd Provider、Durable Job/Approval、Pigsty Integration 与双语 Console。
但“AI-First DBA Agent”不是一个好的架构中心：它容易让 Assistant Workflow 看起来像写入
语义的所有者，也让 Direct、HA 与 Lifecycle 成为彼此平行的产品线。

无论请求来自谁，控制面都必须稳定回答七个问题：

1. 目标 Resource 是什么？
2. 对其身份有多确定？
3. 当前 Effective Capability 是什么，为什么？
4. 准备进行的精确变更是什么？
5. 哪套 Policy 与 Approval 准入它？
6. 哪个 Durable Operation 持有执行与恢复权威？
7. 哪些 Evidence 与 Audit 证明最终结果？

把这些问题移入 Kernel，既能让 Assistant Automation 更安全，也让产品在没有 LLM 时仍然
完整有用。

## Kernel 边界

```text
Actor / Entry Point
        │
        ▼
Resource → Capability → Planner → Policy → Operation → Driver
                                                   │
                                                   ▼
                                                Audit
```

Driver 保留 Provider 原生语义，但不能成为另一套 Planner。Kernel 与 Public Package 不
依赖 Console、License、LLM、Web 或 Legacy Metadata Table。

## 对 Release 的影响

本决策最初把 Research MVP 拆成 v0.3–v0.5 Product Proof，v0.6 随后完成世界合并工作。
这些版本及其 K 系列合同现在作为历史交付与回归证据保留。

CC-CP-007 在不改变本内核决策的前提下，更新了日程与验收方法。当前产品优先列车依次为
v0.7 读侧信任、v0.8 可逆闸门、v0.9 Pigsty 破坏性生命周期、v1.0 Agent 与自动化。
详见[状态与路线图](/zh/docs/develop/roadmap/)。

## 兼容性

重新立项是增量演进。v0.2 Public Package、19 条 CLI、v1alpha1 Schema、UNKNOWN 语义、
Durable Confirmation、Pigsty Safety 与 Release Evidence 永久进入回归合同。

## 依据

- `BOAR-CHARTER.md`
- `_bmad-output/planning-artifacts/control-plane-architecture.md`
- `_bmad-output/planning-artifacts/control-plane-decision-log.md`（ADR-012、ADR-015）
- `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`（ADR-022 至 ADR-025）
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`

v0.7 及以后版本的排期与验收以 CC-CP-007 和上述路线图为准，取代旧的故事级验收框架。
可读文档从[核心概念](/zh/docs/concepts/)开始。
