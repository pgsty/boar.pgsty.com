---
title: Pigsty lifecycle
description: Inspect Pigsty inventory and prepare only sealed, allowlisted actions.
weight: 30
---

Pigsty integration has two separate stages: establish resource evidence, then
plan an allowed lifecycle action. Reading an inventory file is never execution
authority.

> [!NOTE]
> Status on 2026-09-08: v0.7 P5 passed local acceptance for the read-only
> inventory and structured-progress surfaces against a real Pigsty 4.5 lab.
> The acceptance run performed controlled add-replica and service-refresh
> operations to prove the event projection. Inventory editing and general
> lifecycle authoring are later trains; v0.7 is not an official release.

## Parse and import

```bash
boar pigsty parse --file /opt/pigsty/pigsty.yml --summary
boar pigsty import --file /opt/pigsty/pigsty.yml
```

Parsing applies the frozen redaction and source-digest rules. Import commits a
candidate or reconciled graph into Boar metadata; it does not invoke Ansible or
modify the target.

## Inspect the action catalog

```bash
boar pigsty operations
```

The current catalog includes inventory validation, deploy, node add, cluster
initialization, replica add, service refresh, HBA reload, database/user
creation, and destructive instance/cluster removal. Each action declares
required selectors, allowed tags, allowed extra variables, and a legacy safety
level translated conservatively into kernel risk.

There is no arbitrary playbook, arbitrary shell, or arbitrary `--extra-vars`
surface.

## Plan before execution

```bash
boar pigsty plan pgsql.refresh_service --cluster pg-meta
```

A plan binds the exact source digest, action, cluster, hosts, limit, tags, and
allowlisted extra variables. The durable Pigsty driver rechecks those facts
and verifies postconditions.

With any Kernel control lane enabled—as they are by default in Server
mode—`boar pigsty run --execute` deliberately refuses execution. Submit the
sealed Plan through the Kernel Console/API approval and admission path. The
legacy standalone execution switch is available only in a standalone
configuration where all three Kernel write lanes evaluate to disabled; it is
not the Server control path.

> [!DANGER]
> `pgsql.remove_cluster` and `pgsql.remove_instance` are destructive L5 legacy
> actions. They can remove data, backups, packages, or software according to
> explicit flags. Resolve the exact production target and obtain the required
> approval before execution.

## State model

Pigsty resources distinguish desired inventory, recorded control-plane state,
and actual observed state. Drift is information used by a plan; it is not an
instruction to converge automatically.

The accepted v0.7 page shows structured clusters, nodes, inherited parameters,
host packages, SQL extensions, and differences from authorized Direct
observations. Newly listed inventory members that have not been imported as
Resources remain UNKNOWN. Structured progress includes durable per-task
events, node/module/result fields, and safe source locations when available;
display truncation is reported rather than hidden.

Editing `pigsty.yml`, reviewing its diff and history, and executing the change
from the editor belong to v0.9 P11. The inventory file remains the source of
truth.

See [DN-006: Three domains, one authority](/blog/design/three-domains-one-authority/).
