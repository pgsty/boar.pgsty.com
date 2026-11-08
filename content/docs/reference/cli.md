---
title: Command-line interface
description: Current runtime, administration, Pigsty, Site Agent, and Patroni-compatible commands.
weight: 10
---

This reference describes the source CLI as of 2026-09-08. Use
`boar <command> --help` from the exact binary you operate; a released binary is
the final command authority for that version.

## Runtime and administration

| Command | Purpose |
|---|---|
| `boar server` | Run the PostgreSQL-backed shared control plane |
| `boar local` | Run the single-user SQLite control plane |
| `boar agent` | Manage Site Agent initialization, enrollment, identity, and journal |
| `boar migrate` | Apply forward-only metadata migrations |
| `boar version` | Print build, Patroni, and PostgreSQL version information |
| `boar completion` | Generate shell completion |

The current bare `boar` invocation remains a Server compatibility path. New
automation should use `boar server` explicitly.

## Global flags

```text
--config
--database-url
--server-addr
--base-path
--mode
--log-format
--demo
--pigsty-home
--pigsty-inventory
```

## Patroni-compatible commands

Boar keeps 19 commands flat for script compatibility:

| Read and discovery | Routine write | High risk and topology |
|---|---|---|
| `version`, `list`, `topology`, `history`, `show-config`, `dsn`, `query` | `reload`, `restart`, `pause`, `resume`, `flush`, `edit-config` | `switchover`, `failover`, `reinit`, `remove`, `promote-cluster`, `demote-cluster` |
{.wide .expand}

Every command is a native Cobra callback. The release does not invoke Python or
the `patronictl` executable.

`boar discover` is an additional Boar fleet-discovery command. It is not one
of the frozen 19 patronictl-compatible commands.

## Pigsty commands

```text
boar pigsty parse
boar pigsty import
boar pigsty operations
boar pigsty plan ACTION
boar pigsty run ACTION
```

`run` defaults to dry-run. `--execute` requests direct execution, but it is not
sufficient under the default configuration: when any of the three Kernel
control channels is enabled, the command refuses execution and requires exact
Kernel Plan approval and admission. All three channels default to enabled, so
normal writes use the Console or API Plan flow.

## Local commands

```text
boar local
boar local export
```

Local accepts an absolute `--state-dir`, exact loopback `--listen`, optional
guarded `--bootstrap-file`, and `--no-open-browser`. The listen default is
`127.0.0.1:0`; `--bootstrap-file` requires `--no-open-browser`.

## Site Agent commands

```text
boar agent init
boar agent enroll
boar agent identify
boar agent run
boar agent journal
```

All commands require an explicit owner-private agent configuration through
`--agent-config`. `boar agent run` performs one enrollment when needed and
then verifies identity with mTLS. It does not implement the planned persistent
dispatch loop.

## Planned additive names

The frozen v2 CLI contract reserves additive `boar plan` and `boar operation`
surfaces. The current binary exposes neither command in root help. Plans and
Operations are available through the Console and HTTP API, but the reserved
top-level CLI names are not shipped.
