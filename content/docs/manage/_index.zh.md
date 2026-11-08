---
title: 管理 PostgreSQL
description: 在同一控制面合同下使用不同 Provider 的原生工作流。
weight: 30
icon: fa-solid fa-database
sidebar_expanded: true
---

Boar 把 Provider 原生语义保留在类型化 Driver 内部，并在上层提供统一的资源级工作流。

> [!NOTE]
> 截至 2026-09-08，v0.7 P0-P5 已通过本地真实目标验收。签名工件属于本地验收工件，
> 不是正式发布。v0.8 治理代码仍在开发，尚未通过 Epic 或发布列车验收。

已验收的 v0.7 Console 包含舰队总览与统一时间线、Direct DBA 读面与 Session Cancel、
健康报告、集群保护，以及 Pigsty Inventory/Progress 读面。各页面都让缺失或未证明的事实
保持 UNKNOWN。

- [直连 PostgreSQL](direct-postgresql/) — 使用已验收的 DBA 读面检查任意 PostgreSQL URL。
- [Patroni HA](patroni/) — 保留 Patroni 与 DCS 语义以及原生 19 命令兼容。
- [Pigsty 生命周期](pigsty/) — 检查导入的 Inventory 与结构化生命周期证据。
- [Local Mode](local/) — 在已验收边界内运行单用户 SQLite Kernel。
- [Site Agent](site-agent/) — 建立出站 mTLS 身份；通用 Plan 派发仍是 v1.0 P14 工作。
  {.cards}
