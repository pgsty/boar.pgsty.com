---
title: 'DN-009: An evidence-driven release train'
description: Replace progress percentages and person-month promises with dependency and evidence gates.
date: 2026-08-24
lastmod: 2026-09-08
weight: 90
categories: [Engineering]
tags: [evidence, acceptance, release, testing]
series: [Control Plane v2]
---

## Decision

Boar plans and reports the Control Plane train through dependency gates,
parallel work packages, automated validation, real-environment gates, and
provable exits. Person-month estimates and feature-completion percentages are
not the completion model.

## Why percentage complete fails

“The feature is 90% done” cannot answer whether the remaining 10% is a CSS
detail or an untested failover recovery window. In infrastructure control, the
last unproved edge often carries most of the risk.

Likewise, a unit test cannot prove a PostgreSQL transaction boundary, a mock
cannot prove Patroni/etcd behavior, and a component test cannot prove basename,
focus, or reconnection in the real browser.

## Historical Story contract

For the C0–K11 train (v0.3–v0.6), each Story bound numbered KFR/KNR
requirements, dependencies, a parallel group, a minimum evidence class,
Given/When/Then criteria, a candidate receipt, an independent completion
receipt, and cleanup/secret/residue obligations.

Under that historical contract, code without its required evidence stays `in-progress`. Candidate evidence is
the implementation's claim; independent completion is a clean replay of the
exact source by a separate reviewer context.

## Evidence classes

- **static**: types, schemas, unit, fuzz, golden, build, dependency rules;
- **db**: real supported metadata database behavior;
- **lab**: real Patroni, etcd, PostgreSQL, Pigsty, or Site Agent behavior;
- **browser**: user-visible, responsive, keyboard, i18n, and transport behavior;
- **remote-ci**: a named remote run URL and exact commit.

A stronger-looking but different class does not silently substitute for the
required one.

## Receipts and history

Receipts bind source commit, artifact hashes, toolchain, tests, environment,
target-call counts, secrets, and residue. Rejected receipts remain auditable.
A repair produces a successor receipt; it does not erase the finding.

This history matters because many of Boar's strongest contracts came from
counterexamples: lost acknowledgements, forged events, mutated snapshots,
cross-scope cursors, focus loss, unsafe ancestors, and startup replay hazards.

## Current train

CC-CP-007 and ADR-022 replaced that Story-level regime for v0.7 and later work
with product Epics. Each Epic closes with one real-target end-to-end journey
plus clean `make test` and `make lint` runs. Tests follow the working journey,
and added test lines stay at or below one third of added product lines.
Story-level receipts, compatibility manifests, and contractcheck validators are
no longer created for new work. Historical ones remain preserved;
`make check-contract` runs once at the release gate, not as the daily gate.

At the 2026-09-08 snapshot, v0.7 P0–P5 passed the recorded local acceptance on
source `3094b048f6d3510f28688c1507acb9a2d5f6e0ac`. The five P1–P5 journeys,
`make test`, `make lint`, the one release-level contract gate, and four local
platform artifacts are recorded as passing. The evidence explicitly says that
the source and artifacts have not been pushed or formally released. P6–P15 are
outside that acceptance record and must not be inferred complete from code in
the working tree.

## Release meaning

The v0.3–v0.6 proofs remain historical evidence. A successful build, local
acceptance, a locally signed acceptance artifact, pushed source, a Git tag, and
a public release are separate states. The v0.7 signature has scope
`local-acceptance`; it is not a public release signature or release identity.
Current scope and evidence limits are published in
[Status and roadmap](/docs/develop/roadmap/).

Developer reference: [Contracts and evidence](/docs/develop/contracts/).

## Sources

- Historical contract and evidence classes: `BOAR-CHARTER.md` §§5, 10.
- Current train rules: `_bmad-output/implementation-artifacts/correct-course-product-first-train-v0.7.md` and `_bmad-output/planning-artifacts/control-plane-decision-log-amendment-v2.2.0.md` (ADR-022, ADR-025).
- Current Epic scope: `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`.
- v0.7 result and signature scope: `docs/acceptance/v0.7/README.md` and `docs/acceptance/v0.7/release/boar-v0.7.0-build-receipt.json`.
