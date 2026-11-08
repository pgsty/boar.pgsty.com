---
title: Configuration
description: Establish the configuration authority and secret-file boundaries.
weight: 40
---

Boar resolves ordinary settings in this order:

```text
CLI flags > BOAR_* environment > configuration file > defaults
```

This precedence does not mean every sensitive value is accepted through every
source. Security-critical files and raw key material have narrower contracts.

## Production-oriented server example

```yaml
server_addr: 127.0.0.1:9876
base_path: /
database_url: postgres://boar_service@127.0.0.1:5432/boar?sslmode=verify-full
mode: prod
log_format: json
auto_migrate: false
confirmed_execution_timeout_seconds: 3600
```

For production, keep the file canonical, regular, non-symlink, owned by the
service UID, and mode `0600`.

## Control and credential authorities

The active source tree supports separate security-sensitive authorities:

- `control_config_path` selects the Patroni context catalog.
- `control_plan_key_file` contains exactly 32 raw bytes for durable Console plan encryption.
- `credential_master_key_files` maps version names to exact 32-byte key files.
- `credential_active_key_version` selects the key used for new envelopes.
- `license_public_keys` and `license_private_key` configure ES256 license verification and optional issuing.

Control and credential key files must be canonical, owner-private regular
files. Plaintext master keys are not valid inline YAML values.

## Kernel migration switches

`kernel_patroni_restart`, `kernel_patroni_domain`, and
`kernel_postgres_write` are migration gates in the current development tree.
They select a single kernel dispatch authority for the corresponding domain;
they are not permission grants and do not relax Policy.

All three default to `true`, including in `boar.yaml.example`. With those
defaults, legacy Patroni restart/domain writes and `boar pigsty run --execute`
are rejected and directed to exact Kernel Plan approval and admission. Use the
Console or API Plan flow for writes; do not disable the gates to bypass it.

## Pigsty integration

```yaml
pigsty_home: /opt/pigsty
pigsty_inventory_path: /opt/pigsty/pigsty.yml
pigsty_auto_import: false
pigsty_run_timeout_seconds: 3600
```

Inventory import forms a candidate graph. Parsing a file does not authorize a
target mutation.

The complete key inventory is in the [configuration reference](../../reference/configuration/).
