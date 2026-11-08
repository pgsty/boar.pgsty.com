---
title: 'DN-010: The permanent compatibility contract'
description: Evolve Boar through versioned successors without rewriting the historically accepted v0.2 contract.
date: 2026-08-24
lastmod: 2026-09-08
weight: 100
categories: [Compatibility]
tags: [compatibility, v0.2, patroni, schema, migration]
series: [Control Plane v2]
---

## Decision

The v0.2 Fusion acceptance baseline is not disposable scaffolding. Its public packages,
CLI, schemas, machine output, failure semantics, migrations, Pigsty safety, and
release evidence are permanent regression contracts.

Control Plane v2 evolves them through versioned successors and adapters. It
does not edit a frozen schema in place or retire a path because a replacement
looks cleaner.

## Frozen assets

The permanent set includes:

- public `config`, `model`, `patroni`, `dcs`, `dcs/etcd3`, `postgres`, and
  `control` packages;
- all 19 flat Patroni CLI commands and human/JSON/YAML behavior;
- v1alpha1 JSON Schemas, OpenAPI, compatibility manifests, and downstream
  consumer contracts;
- independent Outcome, SendState, and Verification axes;
- no automatic retry for ambiguous writes;
- Console durable confirmation and startup no-replay;
- Pigsty redaction, source digest, and argv/environment allowlists;
- forward-only migrations, append-only audit, and the release/security evidence
  attached to the accepted baseline.

This is a compatibility set, not a claim that every later roadmap capability
already exists. A source digest inside a Pigsty Driver Plan binds the inventory
and playbook sources checked at execution; it is also distinct from signing a
release artifact.

## Successor, not mutation

`plan/v1` succeeds `control.Plan/v1alpha1`; it does not redefine it. Kernel
Operation is the new execution authority while legacy Job remains a
projection/history surface.
Resource APIs can project the old cluster view through an adapter. New CLI
names are additive while the 19 Patroni commands stay flat.

This pattern keeps old clients honest and gives new code one northbound model.

## Differential retirement

A legacy dispatch path can retire only after same-domain differential evidence
proves that the successor preserves required behavior—including failures,
UNKNOWN, machine output, and crash windows. Static code similarity is not
enough.

During migration, feature switches select one authority. Dual execution is a
contract violation even if both calls happen to succeed.

## Historical compatibility window

The original train required Patroni `>=4.0.0,<5.0.0`, etcd3-only behavior, and
no Python or `patronictl` runtime dependency through v0.5. That sentence records
the old window; current compatibility must be read from the pinned manifests
and the [compatibility matrix](/docs/reference/compatibility/).

## Why this is worth the cost

Compatibility gates slow casual refactoring, but they preserve the exact
behaviors automation and operators depend on. They also prevent a rewrite from
silently losing the hardest-won reliability semantics.

Operator reference: [Compatibility matrix](/docs/reference/compatibility/).

## Sources

- Frozen baseline, assets, CKR-018, and CKR-019: `BOAR-CHARTER.md` §§3, 5.
- Accepted ADR wording: `_bmad-output/planning-artifacts/control-plane-decision-log.md` (ADR-001, ADR-004, ADR-006, ADR-013, ADR-014, ADR-016, ADR-017).
- Historical contract preservation after v0.7: `_bmad-output/implementation-artifacts/correct-course-product-first-train-v0.7.md` (D4).
- Current pinned inventories and executable checks: `compatibility/contracts.yaml`, `compatibility/control-plane-contracts.yaml`, `compatibility/patronictl.yaml`, `patroni/compatibility_test.go`, `cmd/boar/cmd/patronictl_commands_test.go`.
