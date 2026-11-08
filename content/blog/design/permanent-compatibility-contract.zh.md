---
title: 'DN-010：永久兼容合同'
description: 通过版本化 Successor 演进 Boar，而不改写历史上已验收的 v0.2 合同。
date: 2026-08-24
lastmod: 2026-09-08
weight: 100
categories: [兼容性]
tags: [兼容性, v0.2, patroni, schema, 迁移]
series: [Control Plane v2]
---

## 决策

v0.2 Fusion 验收基线不是可丢弃脚手架。它的 Public Package、CLI、Schema、Machine Output、
Failure Semantics、Migration、Pigsty Safety 与 Release Evidence 永久进入回归合同。

Control Plane v2 通过 Versioned Successor 与 Adapter 演进，不会就地修改冻结 Schema，
也不会因为替代实现看起来更整洁就退役历史路径。

## 冻结资产

永久集合包括：

- 公共 `config`、`model`、`patroni`、`dcs`、`dcs/etcd3`、`postgres` 与 `control` 包；
- 全部 19 条平铺 Patroni CLI 及 Human/JSON/YAML 行为；
- v1alpha1 JSON Schema、OpenAPI、Compatibility Manifest 与 Downstream Consumer Contract；
- 独立 Outcome、SendState 与 Verification 三轴；
- 模糊写入禁止自动重试；
- Console Durable Confirmation 与 Startup No-replay；
- Pigsty Redaction、Source Digest 与 argv/environment Allowlist；
- Forward-only Migration、Append-only Audit，以及已验收 Baseline 所绑定的 Release/Security Evidence。

这是一组兼容合同，不表示后续路线图中的每项能力都已经实现。Pigsty Driver Plan 中的 Source
Digest 用于绑定执行时复核的 Inventory 与 Playbook Source，也不同于对发布工件做签名。

## 继任，而非修改

`plan/v1` 继任 `control.Plan/v1alpha1`，不重新定义它。Kernel Operation 是新的执行权威，
Legacy Job 继续作为 Projection/History Surface。Resource API 可以通过 Adapter 投影旧 Cluster View。新 CLI
Name 以增量方式加入，19 条 Patroni 命令保持平铺。

这个模式既让旧 Client 保持诚实，也为新代码建立一套北向模型。

## 差分退役

Legacy Dispatch Path 只有在同域 Differential Evidence 证明 Successor 保留必需行为后才能
退役，包括 Failure、UNKNOWN、Machine Output 与 Crash Window。静态代码相似性不够。

迁移期间 Feature Switch 选择唯一 Authority。即使两次调用都碰巧成功，Dual Execution
也属于合同违规。

## 历史兼容窗口

原列车要求到 v0.5 为止保持 Patroni `>=4.0.0,<5.0.0`、只支持 etcd3，并且 Runtime
不依赖 Python 或 `patronictl`。这句话记录旧窗口；当前兼容范围应以固定 Manifest 与
[兼容矩阵](/zh/docs/reference/compatibility/)为准。

## 为什么值得

Compatibility Gate 会减慢随意重构，但能保留 Automation 与 Operator 依赖的精确行为，也
防止 Rewrite 静默丢失最难获得的可靠性语义。

操作参考：[兼容矩阵](/zh/docs/reference/compatibility/)。

## 依据

- 冻结基线、资产、CKR-018 与 CKR-019：`BOAR-CHARTER.md` §3、§5。
- Accepted ADR 原文：`_bmad-output/planning-artifacts/control-plane-decision-log.md`（ADR-001、ADR-004、ADR-006、ADR-013、ADR-014、ADR-016、ADR-017）。
- v0.7 起对历史合同的保留：`_bmad-output/implementation-artifacts/correct-course-product-first-train-v0.7.md`（D4）。
- 当前固定清单与可执行检查：`compatibility/contracts.yaml`、`compatibility/control-plane-contracts.yaml`、`compatibility/patronictl.yaml`、`patroni/compatibility_test.go`、`cmd/boar/cmd/patronictl_commands_test.go`。
