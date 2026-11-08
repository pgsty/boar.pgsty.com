---
title: Boar 文档
linkTitle: 文档
description: 用一套显式、可审计的控制面模型管理 PostgreSQL。
search_keywords: [Boar, PostgreSQL 控制平面, Pigsty, Patroni, 运维]
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

Boar 是 Pigsty 的 PostgreSQL 控制平面：把任意 PostgreSQL 直连、Patroni HA
纳管和 Pigsty 生命周期运维，统一到 Resource、Capability、不可变 Plan、持久化
Operation 与 Audit 模型中。

> [!IMPORTANT]
> 本站保留历史上已验收的 Fusion `v0.2` 合同，并记录当前产品优先列车。v0.7 驾驶舱已在
> 源码 `3094b048…` 上通过本地验收，但尚未正式发布。准确证据边界见
> [状态与路线图](develop/roadmap/)。

## 按任务进入

- [快速上手](start/) — 安装 Boar，启动 Local 或 Server 控制面，完成第一条安全工作流。
- [核心概念](concepts/) — 理解资源、身份、能力、计划、操作与风险。
- [管理 PostgreSQL](manage/) — 使用直连、Patroni、Pigsty、Local Mode 与 Site Agent。
- [参考手册](reference/) — 查询 CLI、HTTP API、配置、错误与兼容合同。
- [管理维护](admin/) — 保护、升级、恢复、审计和日常运行 Boar。
- [开发指南](develop/) — 查看当前状态与路线图，构建仓库并理解验收门禁。
  {.cards}

## 产品边界

Assistant、Console、CLI、API、MCP 与 Site Agent 都是 Actor 或入口，任何入口都
不能绕过内核。合法写入路径再短，也必须经过：

```text
Resource → Capability → Plan → Policy → Operation → Driver → Audit
```

如果你关注架构而非具体操作，请先阅读[控制面内核设计笔记](/zh/blog/design/control-plane-kernel/)。
