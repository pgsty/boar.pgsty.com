---
title: Patroni HA
description: 通过 Boar 原生 SDK 与共享 Kernel 管理 Patroni。
weight: 20
---

Boar Patroni Driver 建立在仓库公共 Go Package 上，不依赖 Python 子进程，也不替换已经
验证的底座，因此保留 v0.2 的 REST、etcd、PostgreSQL、Plan、Verification 与 Failure
Semantics。

> [!NOTE]
> 截至 2026-09-08，v0.7 已针对真实 Patroni 目标完成集群保护读面的本地验收。
> Console 中的一等操作与后置校验旅程属于 v0.8 P8，尚未通过 Epic 或列车验收。

## 支持边界

- Patroni `>=4.0.0,<5.0.0`；已审查 Release `4.0.7` 与 Source Lane `4.1.0`。
- 当前兼容窗口只支持 etcd3 DCS。
- Runtime 不依赖 Python 或 `patronictl`。
- 原生 Cobra 命令保持 Human、JSON 与 YAML 合同。

其他版本是“未经验证”，不是“默认兼容”。

## 十九条兼容命令

当前 CLI 提供：

```text
list      topology  history  show-config  edit-config  version
pause     resume    restart  reload       reinit       switchover
failover  flush     remove   dsn          query        promote-cluster
demote-cluster
```

使用 `boar <command> --help` 查询精确 Flag。这些命令为脚本兼容永久保持平铺，不会移动到
新的 Namespace 下。Boar 还提供额外的 `discover` 命令，但它不属于 19 条
patronictl-compatible 命令。

## Kernel 迁移

既有 `control.Plan/v1alpha1` 继续作为类型化 Patroni Plan。Adapter 将它作为 Driver
Payload 嵌入资源级 Kernel Plan。K2 在已知崩溃窗口中证明 Restart Vertical Slice；K5
把 Patroni Domain 迁移到唯一 Dispatch Authority，同时保留 19 命令差分一致性。

Legacy Route 可以把 Operation 投影为旧 Console Job，但只有 Kernel Lane 能真正调用
Patroni。

Server Mode 的 `kernel_patroni_restart` 与 `kernel_patroni_domain` 默认都是 `true`。
这些开关不授予动作权限；Effective Capability、环境 Policy、精确 Plan 准入、所需审批、
Resource Lock 与 Audit 仍然必须满足。在启用 Kernel 的部署中，会产生写入的平铺兼容
命令拒绝 Standalone 执行，要求精确的 Server Kernel Plan 审批与准入。

## 已验收的保护视图

v0.7 视图组合 Topology、Replication、Routing Evidence、Cluster Instrument 与
pgBackRest Archive Evidence。Pigsty 目标可以读取 VictoriaMetrics；没有 Monitoring
Profile 的目标使用有边界的 Direct Collector。缺少 VIP、HAProxy、PgBouncer、Backup
或 Metrics 通道时保持缺失或 UNKNOWN，不会变成健康的零值。

页面显示的可恢复区间来自已证明的归档链，并不证明真实 Restore 或 PITR 演练成功；这些
旅程安排在 v0.9 P12-P13。

## 安全要点

- Switchover 为 High；Failover 在 Kernel Registry 中固定为 Critical。
- Reload 为 Low，Restart 为 Medium，Reinitialize 为 High。
- DCS Fallback 与 REST Transport Evidence 分别记录。
- Outcome、Send State 与 Verification 三轴独立。
- 模糊 Patroni Write 必须进入 UNKNOWN，禁止自动重试。
- Edit Config 至少为 High，并会根据受影响字段升格到 Critical。

设计理由见 [DN-006](/zh/blog/design/three-domains-one-authority/) 与
[DN-010](/zh/blog/design/permanent-compatibility-contract/)。
