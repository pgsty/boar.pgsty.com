---
title: 直连 PostgreSQL
description: 发现任意 PostgreSQL URL，并且只暴露有证据支持的动作。
weight: 10
---

> [!NOTE]
> 截至 2026-09-08，v0.7 P2 已通过本地真实目标验收，覆盖本地 PostgreSQL 与一个独立的
> RDS 类 PostgreSQL 目标，但没有使用云厂商 RDS 账号。v0.7 尚未正式发布。

Direct Mode 从 Access Path 出发建立 Resource Graph，不会把 DSN 直接当成无需质疑的
资产身份。

## 完整旅程

1. 使用 URL 与 CredentialRef 创建 Connection。
2. 探测 Transport 与 Authentication，不发布任何 Secret Material。
3. 在 Principal 权限范围内发现 PostgreSQL Identity、Version、Role、Database、Setting
   与 Relationship。
4. 将 Observation 匹配到既有 Asset，或提出一个新 Asset。
5. 评估 Intrinsic 与 Effective Capability。
6. 立即暴露只读 Surface；每个写入都必须先创建 Plan。

Connection 与 Credential Record 相互独立。持久化行只保存加密 Credential Envelope，
或包含 Metadata 与 Key Version 的 SecretRef；Resource、Plan、Event 与 Audit 永不保存
明文凭据。

## 已验收的 DBA 读面

Server 端已验收旅程覆盖概览仪表、活动与锁等待树、配置比较、启用
`pg_stat_statements` 时的 Top SQL、需要相应权限的服务端日志读取、对象树、带 EXPLAIN
的保守 SQL 工作区、按用户加密保存的查询历史，以及 pgAdmin `servers.json` 导入。
采集使用 10 秒周期、每条目标查询 100 毫秒硬超时与短期留存样本。

低权限连接仍然有价值：无法检查的字段以带原因的 UNKNOWN 呈现，而不是伪造为空数据。
SQL 工作区是有边界的只读工具，不是完整 pgAdmin，也不提供任意 SQL 写入权威。

## 会话动作与下一趟治理列车

v0.7 真实旅程已证明：Session Cancel 经过可审查的 Immutable Plan、Policy Attestation、
持久 Operation、Verification 与 Audit。Registry 将 Session Cancel 定为 Low，Session
Terminate 定为 Medium。动作是否可用仍只由 Effective Capability 决定；显示按钮本身
不构成执行权威。

早期 K5 类型化写入底座仍然存在：它包含 Create Index 与 Parameter Change Plan，并把
参数变更区分为 Dynamic、Reload 与 Restart。v0.8 在此基础上增加面向产品的集群治理与
统一审批旅程，覆盖参数、数据库、角色、扩展、HBA 校准与临时授权；这些 v0.8 源码仍在
开发，尚未通过 Epic 或列车验收。

Server Mode 的 `kernel_postgres_write` 默认是 `true`，但该开关只让通道进入评估：
Capability、Policy、精确 Plan 准入、Lock 与 Audit 仍然必须满足。任意 SQL Write 不是
北向 Capability，Lost Acknowledgement 也不能触发盲目重放。

## 健康与成本证据

v0.7 已验收健康报告检查膨胀、未使用索引、缺少主键、HBA 与 `trust` 暴露、超级用户、
证书到期、密码状态和保护参数等证据。无法支持或读取的检查保持 UNKNOWN。TCO 面板只按
操作者输入计算，不查询云厂商价格，也不自动换汇。

## 传输安全

尽量使用 `sslmode=verify-full`。Credential、Trust Root、Service File、Passfile 与 TLS
Key File 都有显式来源与权限规则。Channel Binding 为 `require` 时必须实际协商
`SCRAM-SHA-256-PLUS`；不满足时是认证失败，不是 Warning。

生产使用前阅读[安全模型](../../admin/security/)与[兼容矩阵](../../reference/compatibility/)。
