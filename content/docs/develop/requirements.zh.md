---
title: 需求与发布门
description: 当前产品列车退出条件，以及继续用于追溯的历史编号合同。
weight: 30
---

CC-CP-007 之后，产品优先 `control-plane-roadmap-v0.7-v1.0.md` 是计划与验收权威。
Charter 的产品定义与 20 条 CKR 继续有效。编号 PRD、Architecture、K1–K11 Story 与
旧验收合同继续作为历史追溯来源；本站不替代源码仓库中的原始字节。

> **实现快照 — 2026-09-08。** v0.7 P0–P5 已在源码 `3094b048…` 上通过本地验收。
> 制品签名作用域是 `local-acceptance`，v0.7 尚未正式发布。v0.8 正在开发，本快照中没有
> v0.8 验收目录。完整证据边界见[状态与路线图](../roadmap/)。

## 历史编号合同

| 领域 | 需求编号 | 公开合同 |
|---|---:|---|
| 产品公理 | KFR-001–006 | PostgreSQL-only 控制面；AI 是 Actor；每次写入都有 Plan；Driver 不得绕行 |
| Resource 与 Identity | KFR-010–021 | 持久资源、Access Path 分离、多证据身份、显式管理状态 |
| Capability | KFR-030–037 | 固有与有效能力分离；保留 `unknown` 和 `insufficient_privilege` |
| Connection、Discovery、Import | KFR-050–060 | 分阶段探测、部分证据、Candidate Graph、有界 SSH Tunnel |
| Plan、Policy、Approval | KFR-070–081 | 不可变计划哈希、过期检测、作用域策略、职责分离 |
| Durable Operation | KFR-090–103 | 持久 Step、租约、锁、崩溃恢复、有序事件、诚实表达歧义 |
| Driver 与三域 | KFR-120–132 | 类型化 SPI；Patroni、Pigsty 与 SQL 共用一个北向权威 |
| Local 与 Site Agent | KFR-150–157 | 独立 SQLite Store；回环启动；outbound mTLS 类型化执行 |
| Console 与 Assistant | KFR-170–180 | 资源作用域 IA、能力驱动动作、受限 Assistant 与 MCP |
| 认证、密钥、审计、许可 | KFR-190–199 | 作用域授权、CredentialRef、结构化脱敏、追加审计、OSS 可靠性 |
| 系统质量 | KNR-001–020 | 确定性、有界输入、恢复、Store 等价、兼容与证据治理 |
{.wide .expand}

这些编号继续作为稳定追踪键，已经完成的证据保持可审计。原 Story 级完成流程适用于
C0–K11 历史，不再作为 v0.7 起新增工作的验收流程。

## 当前 Epic 退出条件

| 列车 | Epic 退出项 | 当前状态 |
|---|---|---|
| v0.7 驾驶舱 | P0 门禁清障；P1 舰队/时间轴；P2 直连 DBA；P3 健康报告；P4 保护视图；P5 Pigsty 只读 | 六项均已本地验收；等待正式发布 |
| v0.8 可逆闸门 | P6 策略与临时授权；P7 集群治理；P8 Patroni UI；P9 告警收件箱；P10 可操作性 | 正在开发；本快照中尚无验收完成项 |
| v0.9 Pigsty 深度 | P11 清单编辑器；P12 SOP 库；P13 作业恢复演练 | 规划中 |
| v1.0 Agent 与自动化 | P14 Site Agent 派发；P15 初级 DBA 账号与生成客户端 | 规划中 |
{.wide .expand}

每个 Epic 只有在真实目标旅程跑通，且 `make test` 与 `make lint` 全绿后关闭。测试在旅程
跑通后补写，覆盖旅程行为与内核不变量；新增测试行数不超过新增产品行数的三分之一。
完整 `make check-contract` 每趟发布只运行一次。

## 固定产品边界

- 只管理 PostgreSQL；HA 只做 Patroni 系。
- P11 编辑器落地后，`pigsty.yml` 仍是清单真理。
- Boar 负责可扫一眼的仪表与问题面板；Grafana、Alertmanager、VictoriaLogs 负责
  Dashboard、Alert Rule 与 Log Search。
- 托管云 PostgreSQL 通过直连模型覆盖，不单独承诺一套云 Provider。
- 每次写入继续经过 Plan、Policy、Operation、Driver 与 Audit。UNKNOWN 不折叠，模糊写入
  不自动重试，AI 没有审批权。

变更规则见[合同与证据](../contracts/)，决策历史见
[DN-015](/zh/blog/design/contract-decision-map/)。
