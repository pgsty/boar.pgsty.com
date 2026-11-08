---
title: 配置参考
description: 当前 Root 配置及安全敏感值的边界。
weight: 30
---

普通配置优先级是 `CLI > BOAR_* 环境变量 > YAML > 默认值`。所选 Source Ref 中的精确
Struct 与 Example File 是最终权威。

## 核心配置键

| 配置键 | 用途 | 开发示例 |
|---|---|---|
| `server_addr` | HTTP Listen Address | `0.0.0.0:9876` |
| `base_path` | URL Prefix | `/` |
| `database_url` | PostgreSQL Metadata DSN | `postgresql://127.0.0.1:5432/boar?sslmode=prefer` |
| `mode` | `dev` 或 `prod` 行为 | `dev` |
| `log_format` | `text` 或 `json` | `text` |
| `demo` | 写入 Demo Data | `false` |
| `auto_migrate` | 启动时运行元数据迁移 | 示例为 `true`；生产建议显式迁移 |
| `confirmed_execution_timeout_seconds` | Server 持有的已确认 Operation Deadline | `3600` |
| `dev_frontend_url` | 非内嵌后端构建向开发者显示的 Vite URL | `http://127.0.0.1:5173` |
{.wide .expand}

开发样例中包含 `jwt_secret`。任何真实部署都必须替换，并通过批准的 Secret 机制注入。

## Control-plane 文件

| 配置键 | 合同 |
|---|---|
| `control_config_path` | 规范、UID 所有、`0600` 的 Patroni Context Authority |
| `control_plan_key_file` | 包含恰好 32 字节原始数据的规范文件 |
| `credential_master_key_files` | Key Version 到规范、32 字节、仅 Owner 可访问文件的映射 |
| `credential_active_key_version` | 新 Credential Envelope 使用的版本 |

旧 Credential Key Version 必须保留到 Durable Envelope 完成轮换，并且 Retirement Gate
证明没有 Record 仍然需要它。

## Kernel Cutover 配置

| 配置键 | 作用域 | 默认值 |
|---|---|---|
| `kernel_patroni_restart` | 把 Patroni Restart 路由到 Kernel Operation Lane | `true` |
| `kernel_patroni_domain` | 把 Patroni Domain 路由到唯一 Kernel Authority | `true` |
| `kernel_postgres_write` | 把已确认类型化 PostgreSQL Write 路由到 Kernel | `true` |

这些 Flag 选择实现权威，不授予用户权限。使用默认值时，如果历史直接写命令或
`boar pigsty run --execute` 会绕过 Kernel Plan 审批与准入，Boar 将拒绝执行。

## Server 状态与读侧配置

| 配置键 | 用途 |
|---|---|
| `state_dir` | 仅 Owner 可访问的 Server 状态与自动 Credential Key 根目录 |
| `grafana_meta_database_url` | 可选的 Grafana Metadata 发现来源 |
| `pgbackrest_profiles` | Server 持有的 pgBackRest Binary、Config、Stanza 与 Timeout 绑定 |
| `pig_profiles`、`sow_profiles` | 类型化 Package Provider 绑定，Binary 与 Authority File 由 Server 持有 |
| `observe_profiles` | 与 Resource 绑定的 VictoriaMetrics、VictoriaLogs、Grafana 与 Alertmanager 读源 |
| `postgres_dba_profiles` | 精确的 Target 到 Pigsty Baseline 或 Peer 对比绑定 |
| `console_thresholds` | 舰队延迟、备份过期、License 到期与 Observation 过期阈值 |
| `direct_verification_*` | Saved Connection 周期复验的 Interval、Batch 与 Concurrency |
| `timeline_annotations` | 显式启用的 Grafana Annotation Outlet；Token 从仅 Owner 可读文件获取 |

`state_dir` 默认位于平台 User Config Directory 下的 `boar/server`。新 Server 可以在这里
自动创建 `auto-v1` Credential Key Material。必须把该 Key 与元数据库一起备份；缺少它时
无法打开已保存的 Credential Envelope。

## Pigsty 配置

| 配置键 | 用途 |
|---|---|
| `pigsty_home` | 包含 `ansible.cfg`、Inventory 与 Playbook 的 Pigsty Checkout |
| `pigsty_inventory_path` | 精确 Inventory Source |
| `pigsty_auto_import` | 在配置的启动流程中导入 Inventory |
| `pigsty_run_timeout_seconds` | Pigsty Driver Execution 上限 |

## License 配置

`license_public_keys` 接受 PEM 或路径形式的额外 ES256 验签公钥。可选
`license_private_key` 启用签发，必须按 Signing Authority 保护。

## 文件规则

Configuration、Service、Passfile、TLS Private Key、Credential Master Key 与 Release
Signing Key File 都有类型、Owner、Mode 与 Symlink 限制。YAML 能表示一个值，不代表这个
值可以被安全接受。

源码样例：[`boar.yaml.example`](https://github.com/pgsty/boar/blob/main/boar.yaml.example)。
