---
title: 'DN-012：以资源作用域组织 Console'
description: 从 Feature Page 渐进迁移到 Scope、Capability、Plan 与 Operation。
date: 2026-08-24
lastmod: 2026-09-08
weight: 120
categories: [设计]
tags: [console, ux, 导航, scope, 可访问性]
series: [Control Plane v2]
---

## 背景

v0.2 Console 已建立 Overview、DBA Agent、SQL Editor、Cluster Detail、Session、Settings
与兼容 Legacy Route 的双语合同，其路由与行为继续作为回归证据。旧暗色视觉不再是当前
合同；2026-09-04 起已经由亮色默认的设计系统取代。

Control-plane Kernel 引入 Resource、Scope、Capability、Plan、Approval、Operation 与新
Runtime Mode。只是继续增加 Provider Page，会重新制造 Kernel 已经消除的割裂。

## 决策

通过兼容 Route 渐进迁移，而不是一次性推倒重写。当前前端注册的一级导航有八项：

```text
首页
连接
资源
时间轴
变更
观测
治理
设置
```

操作者最常问的七个问题仍是组织模型。「连接」是入口动作，不是第八个问题；同时 v0.7 P1
旅程为了快速跨域查看事件，把「时间轴」提升为独立一级 Route。因此「七个问题」与「八个
导航入口」都是有意设计。

页面用 Workspace、Fleet、Site、Cluster、Instance 与 Database Scope 组织上下文。Provider
具体细节成为 Resource Tab 或 Related Link，而不是一级产品孤岛。旧 `/overview`、`/fleet`、
`/operate` 与 `/chat/:clusterId` Link 继续由 Redirect 或 Compatibility Route 承接。

## Capability 驱动动作

按钮消费 Effective Capability，并区分 Unsupported、Unknown、Denied、Stale、Locked 与
Approval Required Reason，不能从 Provider Text 推断 Authority。

只有一个 Connection/Instance 的 Direct User 应看到简化 Instance Home，而不是空洞 Fleet
机制。为了让页面显得简单，不能把缺失事实解释为“已证明不存在”。

## Plan 与 Operation

Plan Review 展示 Digest、Risk、Step、Precondition、Expiry、Approval 与 Reversibility。
Operation View 在 Reconnect/Scope Change 时保持精确 Identity，重放 Event，并诚实呈现
PARTIAL、UNKNOWN、Compensation Failure、Current Known State 与 Recovery Advice。

## Assistant 集成

既有 Chat Route 与 Block Renderer 保持兼容，同时产品语言转向 Assistant。新 Plan/Operation
Block 使用版本化 Envelope。Assistant 不能通过 UI 获得 Approval 或 Execution Authority。

## 实现状态

旧 K8 工作已在 v0.3–v0.6 列车中交付，现在作为历史回归证据保留。当前源码已经注册统一
资源、时间轴、变更、直连 DBA、健康报告、保护、纳管、Pigsty、观测与治理页面，并由
`/api/v1/console/*` Projection 和 Typed Resource Endpoint 提供数据。v0.7–v1.0 的范围与
验收权威是当前路线图，而不是旧 K8 Story Map，见
[状态与路线图](/zh/docs/develop/roadmap/)。

ADR-023 也取代了旧的「几个查询加深链」读侧解释。Boar 自己拥有可扫一眼的仪表与问题
面板；没有 Pigsty 监控栈的目标也会做有界直连采集：周期 10 秒、单语句硬超时 100 毫秒、
总预算不超过一个周期。Dashboard 编辑、Alert Rule 与 Log Search 仍归 Grafana、
Alertmanager 与 VictoriaLogs；Boar 为它们提供入口、上下文与 Deep Link。

## 可访问性合同

新 Control 必须有翻译名称、Keyboard Focus Behavior、Lucide Icon、CSS-token Color、
Responsive Behavior 与 Browser Evidence。当前主题默认亮色；`[data-mode="dark"]` Token Block
只是预留，尚无 Toggle，Dark Mode 属于 P10。Scope Selection 不能清空无关 Operation
State，也不能暴露另一个 Account/Workspace 的 Stale Authority。

## 当前仓库依据

- `docs/design/console-information-design.md` 与
  `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.1.0.md`：七个问题与
  ADR-019 读模型决策。
- `frontend/src/features/controlPlaneShell/PrimaryNavigation.tsx` 与
  `frontend/src/App.tsx`：实际八项导航与当前 Route Table；较早的「七个一级入口」文字不代表
  当前数量。
- `frontend/UI_UX_ALIGNMENT.md`、`docs/design/console-overhaul-plan.md` 与
  `frontend/src/styles.css`：当前亮色默认视觉合同与延期 Dark Mode。
- `internal/handler/routes.go` 与 `internal/consoleview/`：当前 Console Projection 与 Resource
  Route 实现。
- `internal/postgresdba/types.go` 与
  `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`：ADR-023
  采集边界与观测职责。
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`：当前产品范围、P1
  Timeline 与 P10 Dark Mode 目标。
