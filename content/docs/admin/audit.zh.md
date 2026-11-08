---
title: 审计与证据
description: 保存每个动作的意图、审批、派发、验证与观测责任链。
weight: 30
---

Audit 回答问责问题，Operation Event 回答执行问题。Boar 同时保存两者并建立关联，但不会
混淆它们的权威。

## Audit Record

Audit Entry 标识 Actor、Action、Resource Scope、Request 或 Plan、Policy Decision、
Outcome 与相关 Evidence Reference，不能包含明文 Credential、含 Secret 的 Raw URL 或
Prompt Material。

Audit Table 只追加。生产数据库权限撤销 Update 与 Delete。修正通过新增 Record 表达，
不能改写历史。

## Operation Event Stream

Event 构成单个 Operation 的有序持久序列：Create、Admission、Approval、Lock/Lease
Transition、Step Commitment、Provider Send Fact、Verification、Cancellation、Recovery
与 Terminal Outcome。

用于传输 Event 的 WebSocket/SSE/REST 机制不是 Event Authority。Client 可以从 Sequence
继续读取，并将自身 View 与 Durable Store 对照。

## 开发验收证据

历史列车保留既有 Candidate 与 Completion Receipt。从 v0.7 产品优先列车开始，每个 Epic
统一验收一次：一条真实目标端到端旅程，加 `make test` 与 `make lint`；列车级
`make check-contract` 和签名平台制品只在发布前执行一次。当前开发不再新增故事级 Receipt。

Evidence 记录 Source Commit、Test、Environment Dimension、Target Call、Secret Finding
与 Residue。失败证据仍是历史，修复通过后也不能删除。v0.7 的 P0-P5 Journey 已在
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac` 通过；其签名 Build Receipt Scope 是
`local-acceptance`，不是正式 Release Record。

## 证据等级

| 等级 | 能证明什么 |
|---|---|
| static | Type、Schema、Build、Unit/Fuzz/Golden Contract |
| db | 在真实受支持 Metadata Database 上的行为 |
| lab | 真实 Patroni、etcd、PostgreSQL、Pigsty 或 Site Agent 行为 |
| browser | 固定 Browser 中用户可见行为与可访问性 |
| remote-ci | 具名 Remote Run URL 与精确 Commit |

Static 或 Mock Evidence 不能代替要求的真实环境。

## 事故证据保存

Cleanup 前保存 Immutable Plan、Approval、Operation/Step/Event Record、三条结果轴、Driver
Evidence、Site Agent Journal 与 Target Observation。对导出证据计算 Hash，并记录采集者。
