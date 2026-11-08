---
title: 状态与路线图
description: Boar 已验证实现快照，以及 v0.7 至 v1.0 的产品优先列车。
weight: 5
---

本页明确区分已经实现并验收的能力、正在开发的能力与未来规划。内容于
**2026-09-08** 对照 Boar 源码树及验收证据完成核对。

> [!IMPORTANT]
> v0.7 驾驶舱已经通过本地验收，但尚未推送或正式发布。签名工件的作用域是
> `local-acceptance`，不能当作公开发布制品。

## 当前状态

| 列车 | 范围 | 2026-09-08 状态 |
|---|---|---|
| v0.3–v0.6 | 内核、三域统一、Local 与 Site Agent 原型、Backup/Observe、Console 读模型 | 已在源码列车中交付；历史合同继续作为回归证据 |
| v0.7 | 只读驾驶舱，P0–P5 | 六个 Epic 均通过本地真实目标旅程、`make test`、`make lint`、发布合同门与本地四平台制品验签；尚未正式发布 |
| v0.8 | 可逆操作，P6–P10 | 正在开发；本快照中没有 v0.8 验收目录，因此不宣称任何 Epic 或版本已经完成 |
| v0.9 | Pigsty 破坏性生命周期，P11–P13 | 规划中 |
| v1.0 | Site Agent 派发与自动化，P14–P15 | 规划中 |
{.wide .expand}

“只读驾驶舱”描述的是本趟列车的读侧主线，并不表示整个程序绝无写入。v0.7 仍包含受
Plan 约束的连接保存、成员绑定、Session Cancel/Terminate，以及可选 Grafana Annotation
出口。三条内核写通道默认开启，每项动作仍由 Effective Capability 与 Policy 保护。

## v0.7 验收快照

验收源码为 `3094b048f6d3510f28688c1507acb9a2d5f6e0ac`。六个已验收 Epic 为：

| Epic | 已验收的操作者结果 |
|---|---|
| P0 — 门禁清障 | 日常 `make test`、`make lint` 与发布时合同门分离，历史 Manifest 继续受保护 |
| P1 — 舰队与时间轴 | 舰队健康、变更、Operation、备份、Patroni 历史与 Grafana Annotation 可在统一时间轴中追踪 |
| P2 — 直连 PostgreSQL | 本地与 RDS 类直连目标提供概览、活动、锁等待、配置、Top SQL 与有审计的 Cancel 路径 |
| P3 — 健康报告 | 针对故意配置不当的真实目标命中八类问题，并验证导出与用户输入 TCO 对比 |
| P4 — 保护视图 | 展示拓扑、复制、路由、连接池和可恢复备份窗口；没有监控栈时也能直连自采 |
| P5 — Pigsty 只读 | 在真实 Pigsty 目标上回放清单漂移与结构化生命周期进度 |

最终门禁记录了 817 项前端测试、全绿 `make lint`，并在所有 Epic 旅程之后统一运行一次
`make check-contract`。四平台归档均构建两次并按字节复验，附带校验和、SBOM 与 Ed25519
签名。运行覆盖有两个明确限制：Linux arm64 只完成编译与验签，没有可用运行环境；
Darwin amd64 通过 Rosetta 运行。Linux amd64 与 Darwin arm64 为原生运行。

完整证据与限制见源码仓库的
[v0.7 验收记录](https://github.com/pgsty/boar/blob/c6afd5b9b6d3d722dc6cd791996fa4a0c33d984f/docs/acceptance/v0.7/README.md)。
本快照中该证据提交仍只在本地，推送后链接才可访问；证据绑定的产品源码仍是
`3094b048…`。

## 产品优先列车

当前交付权威是 CC-CP-007、ADR-022 至 ADR-025 接受的
`control-plane-roadmap-v0.7-v1.0.md`。产品定义与 Charter 的 20 条 CKR 不变。旧的编号
PRD、Architecture、K1–K11 Story 与 v0.2 合同继续作为历史和追溯来源。

- **v0.7，读侧信任：** 舰队与时间轴、直连 DBA 读面、健康报告、保护视图、Pigsty
  清单与进度。
- **v0.8，可逆闸门：** 环境与变更策略、临时授权、集群治理、Patroni 一等操作、
  告警、命令面板、OpenAPI 覆盖与经审批的 MCP Apply。
- **v0.9，破坏性生命周期：** 清单编辑器与漂移归零、SOP 模板、作业恢复演练。
- **v1.0，Agent 与自动化：** 生产级 Site Agent 派发，以及受限初级 DBA 账号和生成客户端。

## v0.7 起的验收规则

每个 Epic 用一条面向真实目标的端到端旅程，加全绿 `make test` 与 `make lint` 关闭。
旅程跑通后再补测试，只覆盖内核不变量与旅程本身；新增测试行数不超过新增产品行数的
三分之一。`make check-contract` 只在发布时统一运行一次。历史 Story Receipt、兼容
Manifest 与 Contract Check 继续保留，但新工作不再为每个 Story 增加一套校验器和收据。

内核公理保持不变：每次写入都有不可变 Plan；按钮可用性只来自 Effective Capability；
UNKNOWN 独立且为终态；模糊写入不自动重试；外部调用前先完成 Durable Commit；GUI 不提供
任意 Shell 或 Ansible；AI 没有审批权；凭据不以明文保存。
