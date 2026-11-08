---
title: 驱动
description: 在 Kernel 下保留类型化、有边界的 Provider 语义。
weight: 60
---

Driver 把版本化 Kernel Action 翻译为 Provider 具体工作，不是另一套执行权威。

## Driver 合同

每个 Action 都有封闭 Identity 与类型化 Payload。Driver 声明支持、校验 Payload、准备调用、
报告 Send State、验证 Postcondition 并返回结构化 Evidence，但不能绕过 Planner、Policy、
Operation 或 Audit。

Kernel 在调用 Driver 前先持久化 Step Commitment。Driver 不判断调用者是否有权执行，也不
另写一套审计历史。

## 首批管理域

- **Patroni Driver** 建立在仓库公共 `patroni`、`dcs`、`dcs/etcd3`、`postgres` 与
  `control` 包之上，永久保留 19/19 原生命令兼容与冻结故障语义。
- **PostgreSQL Driver** 发现任意连接，并暴露类型化读动作。早期 K5 类型化写入底座包含
  Create Index 与 Parameter Change Plan；Session Cancel 已在 v0.7 产品旅程验收。v0.8
  在此基础上增加集群治理与统一审批 UX，仍在开发且尚未通过 Epic 或列车验收。Raw SQL
  Write 不是北向 Action。
- **Pigsty Driver** 保留 Source Digest、Redaction、argv/environment Allowlist 与
  Postcondition Verification；GUI 永远不能提交任意 Ansible 或 Shell。
- **Site Agent 原型** 证明 Enrollment、出站 mTLS Identity、Typed Protocol Boundary 与
  Journal Semantics。当前 `agent run` 只做身份检查，不轮询或执行 Plan 任务。

Backup、Package/Repository、Observe 与 SSH Tunnel Provider 合同来自早期 K9 线路。
当前产品列车按用户可见旅程分别验收：v0.7 覆盖读侧仪表与证据，v0.8 覆盖可逆治理，
v0.9 P12-P13 覆盖 PITR 模板与真实恢复演练，v1.0 P14 才把 Site Agent 变成通用 Plan
派发通道。源码存在本身不代表相应旅程已经验收。

## 唯一派发权威

迁移期间 Legacy Endpoint 可以保留，但同一管理域只能有一条 Side-effect Dispatch Lane。
Adapter 可以把 Kernel Operation 投影回 Legacy Job，却不能触发第二次 Provider Call。

设计理由见 [DN-006：三个管理域，一套派发权威](/zh/blog/design/three-domains-one-authority/)。
