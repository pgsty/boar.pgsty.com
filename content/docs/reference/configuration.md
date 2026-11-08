---
title: Configuration reference
description: Current root settings and the boundaries that apply to sensitive values.
weight: 30
---

Ordinary configuration precedence is `CLI > BOAR_* environment > YAML >
defaults`. The exact struct and example file in the selected source ref are the
final authority.

## Core keys

| Key | Purpose | Development example |
|---|---|---|
| `server_addr` | HTTP listen address | `0.0.0.0:9876` |
| `base_path` | URL prefix | `/` |
| `database_url` | PostgreSQL metadata DSN | `postgresql://127.0.0.1:5432/boar?sslmode=prefer` |
| `mode` | `dev` or `prod` behavior | `dev` |
| `log_format` | `text` or `json` | `text` |
| `demo` | Seed demo data | `false` |
| `auto_migrate` | Run metadata migration on startup | `true` in the example; prefer explicit migration in production |
| `confirmed_execution_timeout_seconds` | Server-owned confirmed operation deadline | `3600` |
| `dev_frontend_url` | Vite URL advertised by non-embedded backend builds | `http://127.0.0.1:5173` |
{.wide .expand}

`jwt_secret` appears in the development example. Replace it for every real
deployment and inject it through an approved secret mechanism.

## Control-plane files

| Key | Contract |
|---|---|
| `control_config_path` | Canonical, UID-owned `0600` Patroni context authority |
| `control_plan_key_file` | Canonical file containing exactly 32 raw bytes |
| `credential_master_key_files` | Map from key version to canonical 32-byte owner-private file |
| `credential_active_key_version` | Version used for new credential envelopes |

Old credential key versions remain configured until durable envelopes have
been rotated and a retirement gate proves no record still needs them.

## Kernel cutover keys

| Key | Scope | Default |
|---|---|---|
| `kernel_patroni_restart` | Route Patroni restart through the Kernel Operation lane | `true` |
| `kernel_patroni_domain` | Route the Patroni domain through the single kernel authority | `true` |
| `kernel_postgres_write` | Route confirmed typed PostgreSQL writes through the kernel | `true` |

These flags select implementation authority; they do not grant user authority.
With the defaults, legacy direct writes and `boar pigsty run --execute` are
rejected when they would bypass Kernel Plan approval and admission.

## Server state and read-side settings

| Key | Purpose |
|---|---|
| `state_dir` | Owner-private Server state and auto-provisioned credential-key root |
| `grafana_meta_database_url` | Optional Grafana metadata source used for discovery |
| `pgbackrest_profiles` | Server-owned pgBackRest executable, config, stanza, and timeout bindings |
| `pig_profiles`, `sow_profiles` | Typed package-provider bindings with server-owned binaries and authority files |
| `observe_profiles` | Resource-bound VictoriaMetrics, VictoriaLogs, Grafana, and Alertmanager read sources |
| `postgres_dba_profiles` | Exact target-to-Pigsty-baseline or peer comparison bindings |
| `console_thresholds` | Fleet lag, stale backup, expiring license, and stale observation thresholds |
| `direct_verification_*` | Periodic saved-connection re-verification interval, batch, and concurrency |
| `timeline_annotations` | Opt-in Grafana annotation outlet; its token is read from an owner-private file |

`state_dir` defaults to the platform user-config directory under
`boar/server`. A fresh Server may provision `auto-v1` credential key material
there. Back up that key with the metadata database: stored credential
envelopes cannot be opened without it.

## Pigsty keys

| Key | Purpose |
|---|---|
| `pigsty_home` | Pigsty checkout containing `ansible.cfg`, inventory, and playbooks |
| `pigsty_inventory_path` | Exact inventory source |
| `pigsty_auto_import` | Import inventory during configured startup flow |
| `pigsty_run_timeout_seconds` | Upper bound for a Pigsty driver execution |

## License keys

`license_public_keys` accepts additional ES256 verification public keys by PEM
or path. Optional `license_private_key` enables issuing and must be protected as
a signing authority.

## File rules

Configuration, service, passfile, TLS private-key, credential master-key, and
release signing-key files have type, owner, mode, and symlink restrictions.
Do not assume a value is safe merely because YAML can represent it.

Source example: [`boar.yaml.example`](https://github.com/pgsty/boar/blob/main/boar.yaml.example).
