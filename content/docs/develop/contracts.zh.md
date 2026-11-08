---
title: 合同与证据
description: 把产品需求转化为机器校验、独立重放的退出条件。
weight: 20
---

Boar 不用传统人月估算调度 Control Plane Release Train。v0.7 起，进度以操作者可感知的
Epic、真实目标旅程、日常 Test/Lint 门与发布级合同检查表达。

## Source of Truth 顺序

仓库内文档冲突按以下顺序裁决：

1. 当前用户显式指令；
2. `BOAR-CHARTER.md` 的产品定义与 20 条 CKR；
3. 当前 Epic 与验收权威 `control-plane-roadmap-v0.7-v1.0.md`；
4. 编号 PRD、Architecture 与 Accepted ADR，作为历史和追溯；
5. 用于永久 Legacy Compatibility 的 v0.2 Fusion Contract；
6. 研究文档只作背景。

CC-CP-007 与 ADR-022 至 ADR-025 记录这次变更，不改写旧合同字节。

## 发布映射

| 仓库材料 | 本站公开归宿 |
|---|---|
| Charter 与 Control Plane PRD | [核心概念](/zh/docs/concepts/)和[需求与发布门](../requirements/) |
| Architecture 与 Accepted ADR | [设计笔记](/zh/blog/design/)和[决策总表](/zh/blog/design/contract-decision-map/) |
| 当前 Epic 与验收 | [状态与路线图](../roadmap/) |
| 历史 Epic、Progress 与 Receipt | 本页证据模型与带日期的设计笔记 |
| Fusion v0.2 合同与 Runbook | [兼容性](/zh/docs/reference/compatibility/)、[管理维护](/zh/docs/admin/)与 [v0.2.0 发布注记](/zh/blog/release/v0.2.0/) |
| Package、CLI、API、配置与测试 | [参考手册](/zh/docs/reference/)与[开发指南](/zh/docs/develop/) |
| 研究蓝图与移植研究 | 设计笔记，并明确标记为设计理由而非已发布行为 |

Story 文件和原始 Receipt 继续留在源码仓库：它们是 Review Evidence，不是最终用户
导航。本站沉淀其中的持久决策与操作合同，而不是复制项目管理日志。

## 历史 Requirement 与 Story 合同

旧 v2 Train 包含 125 项 KFR/KNR 与 C0、K1–K9 中的 48 个 Story。每个历史 Story 声明：

- 实现哪些 Requirement；
- Dependency 与 Parallel Group；
- Minimum Evidence Class；
- Given/When/Then Acceptance Criteria；
- Candidate 与 Independent Completion Receipt；
- Cleanup、Secret 与 Residue 约束。

这些记录继续作为永久追溯与回归证据。v0.7 起不再要求新增 Story Receipt 或按 Story
编写 Contract Checker。

## 当前快照

截至 2026-09-08，v0.7 P0–P5 已在源码 `3094b048…` 上通过本地验收；四平台签名制品的
作用域为 `local-acceptance`，并非正式发布。v0.8 P6–P10 正在开发，本快照中没有验收
目录。P11–P15 仍在规划中。

每个新 Epic 用一条对真实目标的端到端旅程，加全绿 `make test` 与 `make lint` 关闭。
旅程跑通后再补测试，新增测试行数不超过新增产品行数的三分之一。完整
`make check-contract` 每趟发布只运行一次。

## 变更控制

修改冻结 CKR、Risk Mapping、Compatibility Promise 或永久内核公理，必须有
ADR/Correct Course 与 Impact Analysis。当前 Epic 范围在权威路线图中演进；历史合同字节
和 Rejected Receipt 必须保持可审计。

另见[状态与路线图](../roadmap/)及历史设计笔记
[DN-009：证据驱动的 Release Train](/zh/blog/design/evidence-driven-release-train/)。
