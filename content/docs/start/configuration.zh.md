---
title: 配置
description: 建立配置权威与 Secret 文件边界。
weight: 40
---

Boar 按以下优先级解析普通配置：

```text
CLI Flag > BOAR_* 环境变量 > 配置文件 > 默认值
```

这种优先级不代表所有敏感值都能通过任意来源注入。安全关键文件与原始 Key Material 有
更严格的独立合同。

## 面向生产的 Server 示例

```yaml
server_addr: 127.0.0.1:9876
base_path: /
database_url: postgres://boar_service@127.0.0.1:5432/boar?sslmode=verify-full
mode: prod
log_format: json
auto_migrate: false
confirmed_execution_timeout_seconds: 3600
```

生产配置必须是规范、普通、非符号链接文件，由 Service UID 持有，权限为 `0600`。

## Control 与 Credential 权威

当前源码树把安全敏感权威拆分为：

- `control_config_path`：选择 Patroni Context Catalog。
- `control_plan_key_file`：保存恰好 32 字节的 Durable Console Plan 加密原始密钥。
- `credential_master_key_files`：把 Key Version 映射到恰好 32 字节的 Key File。
- `credential_active_key_version`：选择新 Envelope 使用的 Key。
- `license_public_keys` 与 `license_private_key`：配置 ES256 License 验签和可选签发。

Control 与 Credential Key File 必须是规范、仅 Owner 可读的普通文件。明文 Master Key 不是
合法的内联 YAML 值。

## Kernel 迁移开关

当前开发树中的 `kernel_patroni_restart`、`kernel_patroni_domain` 与
`kernel_postgres_write` 是迁移门：它们为对应管理域选择唯一 Kernel Dispatch Authority，
不是授权开关，也不会放宽 Policy。

三者默认值均为 `true`，`boar.yaml.example` 也显式如此配置。在这组默认值下，历史
Patroni Restart/Domain 写命令和 `boar pigsty run --execute` 会被拒绝，并要求走精确的
Kernel Plan 审批与准入。写操作应使用 Console 或 API 的 Plan 流程，不能通过关闭迁移门
绕过它。

## Pigsty 集成

```yaml
pigsty_home: /opt/pigsty
pigsty_inventory_path: /opt/pigsty/pigsty.yml
pigsty_auto_import: false
pigsty_run_timeout_seconds: 3600
```

Inventory Import 只形成 Candidate Graph。解析文件本身不会授权目标变更。

完整配置键清单见[配置参考](../../reference/configuration/)。
