---
title: Pigsty 生命周期
description: 检查 Pigsty Inventory，并且只准备密封、白名单化的动作。
weight: 30
---

Pigsty 集成包含两个严格分离的阶段：先建立资源事实，再计划获准的生命周期动作。读取
Inventory File 永远不等于取得执行权威。

> [!NOTE]
> 截至 2026-09-08，v0.7 P5 已在真实 Pigsty 4.5 实验环境通过清单与结构化进度读面的
> 本地验收。验收期间受控执行了 Add Replica 与 Service Refresh，用来证明 Event 投影。
> Inventory 编辑和通用生命周期编排属于后续列车；v0.7 尚未正式发布。

## 解析与导入

```bash
boar pigsty parse --file /opt/pigsty/pigsty.yml --summary
boar pigsty import --file /opt/pigsty/pigsty.yml
```

Parse 使用冻结的 Redaction 与 Source Digest 规则。Import 把 Candidate 或 Reconciled
Graph 提交到 Boar Metadata，不调用 Ansible，也不修改目标。

## 查看动作目录

```bash
boar pigsty operations
```

当前目录包含 Inventory Validation、Deploy、Node Add、Cluster Initialization、Replica
Add、Service Refresh、HBA Reload、Database/User Creation，以及破坏性的 Instance/Cluster
Removal。每个 Action 都声明 Required Selector、Allowed Tag、Allowed Extra Variable 与
Legacy Safety Level，并被保守映射到 Kernel Risk。

系统不存在任意 Playbook、任意 Shell 或任意 `--extra-vars` Surface。

## 执行前先创建 Plan

```bash
boar pigsty plan pgsql.refresh_service --cluster pg-meta
```

Plan 绑定精确 Source Digest、Action、Cluster、Host、Limit、Tag 与白名单 Extra
Variable。Durable Pigsty Driver 会重新校验这些事实并验证 Postcondition。

只要任意 Kernel 控制通道启用，`boar pigsty run --execute` 就会明确拒绝执行；Server
Mode 默认正是如此。应通过 Kernel Console/API 的审批与准入路径提交密封 Plan。只有在
全部三条 Kernel 写通道均计算为 Disabled 的 Standalone 配置中，历史执行开关才可用；
它不是 Server 控制路径。

> [!DANGER]
> `pgsql.remove_cluster` 与 `pgsql.remove_instance` 是破坏性 L5 历史动作；显式 Flag
> 可以令它们删除数据、备份、软件包或软件。执行前必须解析精确生产目标，并取得所需审批。

## 状态模型

Pigsty Resource 区分 Desired Inventory、Recorded Control-plane State 与 Actual Observed
State。Drift 是 Plan 使用的信息，不是自动收敛指令。

v0.7 已验收页面展示结构化 Cluster、Node、继承后参数、Host Package、SQL Extension，
以及与已授权 Direct Observation 的差异。清单中新出现但尚未 Import 为 Resource 的成员
保持 UNKNOWN。结构化进度包括持久化的逐任务 Event、Node/Module/Result 字段，以及可用
时的安全 Source Location；显示截断会明确提示。

在编辑器中修改 `pigsty.yml`、审查 Diff 与历史并执行变更属于 v0.9 P11；Inventory File
继续是 Source of Truth。

设计理由见 [DN-006：三个管理域，一套权威](/zh/blog/design/three-domains-one-authority/)。
