---
title: 'DN-015：Control Plane v2 决策地图'
description: 原始 Accepted ADR 目录、当前修订及每项决策的公开说明位置。
date: 2026-08-24
lastmod: 2026-09-08
weight: 150
categories: [架构]
tags: [adr, 决策, 追踪, 合同]
series: [Control Plane v2]
---

冻结的 Control Plane v2 Decision Log 包含最初 18 项 Accepted ADR。后续 Amendment 只追加
决策，不改写这段历史。本页同时展示两层决策；当前交付范围来自产品优先路线图。

| ADR | 已接受决策 | 公开说明 |
|---|---|---|
| 001 | 把 v0.2 Baseline 锚定到已审查 Commit；Release Promotion 独立进行 | [永久兼容](../permanent-compatibility-contract/) |
| 002 | 仓库公共 Package 是 Canonical Patroni Driver | [三个管理域](../three-domains-one-authority/) |
| 003 | AI Actor 称 Assistant；执行组件称 Site Agent | [Assistant](../assistant-is-an-actor/)、[运行模式](../runtime-modes-and-site-agent/) |
| 004 | `plan/v1` 是资源级 Successor，嵌入 Typed Legacy Payload | [Plan 与 Operation](../immutable-plan-durable-operation/) |
| 005 | Kernel Risk 为 Read/Low/Medium/High/Critical/BreakGlass | [风险参考](/zh/docs/concepts/risk/) |
| 006 | Operation 是执行权威；Job 保留为 Projection/History | [Plan 与 Operation](../immutable-plan-durable-operation/) |
| 007 | Server 用 PostgreSQL Store；Local 独立实现 SQLite Store | [运行模式](../runtime-modes-and-site-agent/) |
| 008 | Durable Ordered Event 是合同；WS/REST/SSE 是 Adapter | [Operation 参考](/zh/docs/concepts/operations/) |
| 009 | 保持 Echo、React 19、Router 7、Zustand、React Query 与 Embedded Frontend | [仓库架构](/zh/docs/develop/repository/) |
| 010 | 新表从第一天带 `workspace_id`；首版创建单 Default Workspace | [资源身份](../resource-identity-and-adoption/) |
| 011 | 核心可靠性属于 OSS；Enterprise 限制组织/合规复杂度 | [OSS 边界](../oss-reliability-boundary/) |
| 012 | Assistant/OODA 作为 Feature 保留；全部副作用迁到 Kernel Plan | [Assistant](../assistant-is-an-actor/) |
| 013 | 到 v0.5 保持 Patroni 4.x、etcd3-only、无 Python Runtime 依赖 | [兼容性](../permanent-compatibility-contract/) |
| 014 | v0.2 SDK、CLI、Schema、API 与 Migration 成为永久 Gate | [兼容性](../permanent-compatibility-contract/) |
| 015 | 把 Research MVP 拆成 v0.3/v0.4/v0.5 Product Proof | [Kernel](../control-plane-kernel/)、[证据 Train](../evidence-driven-release-train/) |
| 016 | 增量加入 `server/local/agent/plan/operation`；保持 Bare Server 与 Flat Patroni CLI 兼容 | [CLI 参考](/zh/docs/reference/cli/) |
| 017 | 把 Approval 泛化为绑定 Plan Hash 的 Policy；新 API 使用 Idempotency/Condition | [Plan 与 Operation](../immutable-plan-durable-operation/) |
| 018 | SSH Tunnel/Backup 属于 v0.5；Restore/PITR 属于 v1；Major Upgrade/DR 属于 v2 | [Driver 参考](/zh/docs/concepts/drivers/) |
{.wide .expand}

ADR-013、ADR-015 与 ADR-018 的版本日程描述原列车。v2.1.0 与 v2.2.0 Amendment
继续追加决策序列：

| ADR | 已接受修订 | 公开说明 |
|---|---|---|
| 019 | 增加服务端只读 `consoleview` Projection；它派生操作者答案，但不成为新的真相源 | [仓库架构](/zh/docs/develop/repository/) |
| 020 | 通过追加式修订增加 v0.6 K10/K11 列车，把历史追溯扩展到 134 项需求与 54 个 Story | [合同与证据](/zh/docs/develop/contracts/) |
| 021 | 沿 First-parent 链审计 F8 发布生命周期，同时保留状态边、Manifest 与 Receipt 规则 | [构建与测试](/zh/docs/develop/testing/) |
| 022 | 按信任顺序建造，每次验收一个操作者可感知的 Epic；日常 Test/Lint，每趟发布统一跑一次完整合同门 | [状态与路线图](/zh/docs/develop/roadmap/) |
| 023 | Boar 负责仪表与问题面板，包括直连轮询与短保留趋势；Grafana、Alertmanager、VictoriaLogs 负责 Dashboard、Alert Rule 与 Log Search | [状态与路线图](/zh/docs/develop/roadmap/) |
| 024 | 内核写通道默认开启，由环境 × 风险 Policy 保护 | [Capability](/zh/docs/concepts/capabilities/) |
| 025 | 指令文件是活文档，验证代码有明确预算 | [构建与测试](/zh/docs/develop/testing/) |
{.wide .expand}

ADR-023 明确放宽了旧的“查询键加 Deep Link”边界。对没有 Pigsty 监控栈的目标，直连采集
合同是 10 秒周期、每条查询 100 毫秒硬超时、总超时不超过一个周期。Deep Link 继续属于
集成边界，但不再是 Boar 读面的全部。

上表记录 Accepted Decision，不表示 Release Promotion。当前源码中，ADR-024 的三个配置默认值
与 `boar.yaml.example` 均为 `true`；完整的环境 × 风险 P6 旅程仍不在 v0.7 本地验收记录内。
同理，P7–P15 已进入 Accepted Scope，也不等于这些 Epic 的验收旅程已经通过。

## 变更规则

`accepted` 表示 Implementation 必须遵守，直到 Successor ADR 或 Correct Course 修订它。
后继决策保留旧文本，并记录新范围与影响。

## 规范来源

Charter 持有产品定义与 CKR，v0.7–v1.0 路线图持有当前 Epic 与验收，Decision Log 及其
Amendment 持有已接受架构决策。本页只是面向读者的索引，不替代仓库源文件。

## 依据

- 产品定义、CKR 与冻结 Source 顺序：`BOAR-CHARTER.md` §1、§4、§5。
- ADR-001–018：`_bmad-output/planning-artifacts/control-plane-decision-log.md`。
- ADR-019–021：`_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.1.0.md`。
- ADR-022–025：`_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md`。
- 当前 Epic 权威：`_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`。
- v0.7 验收边界：`docs/acceptance/v0.7/README.md`。
- 已实现的 ADR-024 默认值：`internal/config/config.go`、`boar.yaml.example`。
