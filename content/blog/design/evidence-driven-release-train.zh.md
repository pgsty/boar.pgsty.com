---
title: 'DN-009：证据驱动的 Release Train'
description: 用 Dependency/Evidence Gate 替代进度百分比与人月承诺。
date: 2026-08-24
lastmod: 2026-09-08
weight: 90
categories: [工程]
tags: [证据, 验收, 发布, 测试]
series: [Control Plane v2]
---

## 决策

Boar 通过 Dependency Gate、Parallel Work Package、Automated Validation、
Real-environment Gate 与 Provable Exit 计划和汇报 Control Plane Train。Person-month
Estimate 与 Feature Completion Percentage 不是完成模型。

## 为什么百分比失效

“功能完成 90%”无法说明剩余 10% 是 CSS 细节，还是尚未验证的 Failover Recovery Window。
在基础设施控制中，最后一个未证明边缘往往携带大部分风险。

同样，Unit Test 不能证明 PostgreSQL Transaction Boundary，Mock 不能证明 Patroni/etcd
行为，Component Test 也不能证明真实 Browser 中的 Basename、Focus 或 Reconnection。

## 历史 Story 合同

C0–K11 列车（v0.3–v0.6）中，每个 Story 绑定编号 KFR/KNR、Dependency、Parallel Group、
Minimum Evidence Class、Given/When/Then Criteria、Candidate Receipt、Independent
Completion Receipt 与 Cleanup/Secret/Residue Obligation。

在这份历史合同中，代码缺少必需证据时保持 `in-progress`。Candidate Evidence 是 Implementation Claim；
Independent Completion 由独立 Review Context 对精确 Source 做 Clean Replay。

## 证据等级

- **static**：Type、Schema、Unit、Fuzz、Golden、Build、Dependency Rule；
- **db**：真实受支持 Metadata Database 行为；
- **lab**：真实 Patroni、etcd、PostgreSQL、Pigsty 或 Site Agent 行为；
- **browser**：用户可见、响应式、键盘、i18n 与 Transport 行为；
- **remote-ci**：具名 Remote Run URL 与精确 Commit。

看似“更强”但不同的 Evidence Class 不能静默替代合同要求。

## Receipt 与历史

Receipt 绑定 Source Commit、Artifact Hash、Toolchain、Test、Environment、Target-call
Count、Secret 与 Residue。Rejected Receipt 保持可审计；Repair 产生 Successor Receipt，
而不是删除 Finding。

这段历史非常重要，因为 Boar 的许多强合同来自 Counterexample：Lost Acknowledgement、
Forged Event、Mutated Snapshot、Cross-scope Cursor、Focus Loss、Unsafe Ancestor 与 Startup
Replay Hazard。

## 当前 Train

CC-CP-007 与 ADR-022 从 v0.7 起用产品 Epic 取代上述 Story 级制度。每个 Epic 以一条真实
目标端到端旅程，加全绿 `make test` 与 `make lint` 关闭。旅程跑通后再补测试，新增测试
行数不超过新增产品行数的三分之一。新工作不再新增 Story 级 Receipt、Compatibility
Manifest 与 Contractcheck Validator；历史产物继续保留。`make check-contract` 只在发布门
运行一次，不再是日常门禁。

在 2026-09-08 快照中，v0.7 P0–P5 已在源码
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac` 上完成有记录的本地验收：P1–P5 五条旅程、
`make test`、`make lint`、一次发布级合同门和四平台本地工件均有通过记录。证据同时明确：
源码与工件尚未推送，也未正式发布。P6–P15 不在这份验收记录内，不能从当前工作树已有代码
推断为完成。

## Release 的含义

v0.3–v0.6 的 Product Proof 继续作为历史证据。Build 成功、本地验收、本地签名验收工件、
源码推送、Git Tag 与公开发布是不同状态。v0.7 签名的 Scope 是 `local-acceptance`，不代表
正式发布签名或发布身份。当前范围与证据限制见
[状态与路线图](/zh/docs/develop/roadmap/)。

开发参考：[合同与证据](/zh/docs/develop/contracts/)。

## 依据

- 历史合同与证据等级：`BOAR-CHARTER.md` §5、§10。
- 当前列车规则：`_bmad-output/implementation-artifacts/correct-course-product-first-train-v0.7.md` 与 `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`（ADR-022、ADR-025）。
- 当前 Epic 范围：`_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`。
- v0.7 结果与签名 Scope：`docs/acceptance/v0.7/README.md` 与 `docs/acceptance/v0.7/release/boar-v0.7.0-build-receipt.json`。
