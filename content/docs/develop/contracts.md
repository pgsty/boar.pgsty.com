---
title: Contracts and evidence
description: Turn product requirements into mechanically checked, independently replayed exits.
weight: 20
---

Boar does not schedule the Control Plane train around person-month estimates.
Since v0.7, progress is expressed through operator-visible Epics, real-target
journeys, everyday test/lint gates, and a release-level contract check.

## Source-of-truth order

Within the repository, conflicting design material is resolved by:

1. current explicit user direction;
2. `BOAR-CHARTER.md` product definition and 20 CKRs;
3. `control-plane-roadmap-v0.7-v1.0.md` for current Epics and acceptance;
4. the numbered PRD, architecture, and accepted ADRs as history and traceability;
5. v0.2 Fusion contracts for permanent legacy compatibility;
6. research documents as informative background.

CC-CP-007 and ADR-022 through ADR-025 record this change without rewriting
earlier contract bytes.

## Publication map

| Repository material | Public home in this site |
|---|---|
| Charter and Control Plane PRD | [Core concepts](/docs/concepts/) and [requirements and release gates](../requirements/) |
| Architecture and accepted ADRs | [Design notes](/blog/design/) and the [decision map](/blog/design/contract-decision-map/) |
| Current Epics and acceptance | [Status and roadmap](../roadmap/) |
| Historical Epics, progress, and receipts | This evidence model and the dated design notes |
| Fusion v0.2 contracts and runbooks | [Compatibility](/docs/reference/compatibility/), [administration](/docs/admin/), and [v0.2.0 release notes](/blog/release/v0.2.0/) |
| Package, CLI, API, configuration, and tests | [Reference](/docs/reference/) and [development](/docs/develop/) |
| Research blueprints and transplant studies | Design notes, clearly labeled as rationale rather than shipped behavior |

Story files and raw receipts stay in the source repository: they are review
evidence, not end-user navigation. Their durable decisions and operating
contracts are distilled here instead of copied as project-management logs.

## Historical Requirement and Story contract

The original v2 train contains 125 numbered KFR/KNR requirements and 48 Stories
across C0 and K1–K9. Each historical Story names:

- requirements implemented;
- dependencies and parallel group;
- minimum evidence class;
- Given/When/Then acceptance criteria;
- candidate and independent completion receipts;
- cleanup, secret, and residue constraints.

Those records remain permanent traceability and regression evidence. From v0.7
onward, they do not require new Story receipts or per-Story contract checkers.

## Current snapshot

As of 2026-09-08, v0.7 P0–P5 have passed local acceptance on source
`3094b048…`; the signed four-platform artifacts have `local-acceptance` scope
and are not a formal release. v0.8 P6–P10 are in development and have no
acceptance directory in this snapshot. P11–P15 remain planned.

Each new Epic closes with one end-to-end journey against a real target plus
clean `make test` and `make lint` runs. Tests follow the working journey, and
new test lines stay at or below one third of new product lines. The full
`make check-contract` is a once-per-release gate.

## Change control

Changing a frozen CKR, risk mapping, compatibility promise, or permanent kernel
axiom requires an ADR or Correct Course and impact analysis. Current Epic scope
changes in the authoritative roadmap; historical contract bytes and rejected
receipts remain auditable.

See [Status and roadmap](../roadmap/) and the historical
[DN-009: Evidence-driven release train](/blog/design/evidence-driven-release-train/).
