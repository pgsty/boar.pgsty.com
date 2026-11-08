---
title: Audit and evidence
description: Preserve who intended, approved, dispatched, verified, and observed every action.
weight: 30
---

Audit answers accountability questions; Operation events answer execution
questions. Boar keeps both and links them without conflating their authority.

## Audit record

An audit entry identifies the actor, action, resource scope, request or plan,
policy decision, outcome, and relevant evidence references. It must not contain
plaintext credentials, raw secret-bearing URLs, or prompt material.

The audit table is append-only. Production database grants revoke update and
delete. Corrections are new records, not rewritten history.

## Operation event stream

Events form an ordered durable sequence for one Operation: creation, admission,
approval, lock and lease transitions, step commitments, provider send facts,
verification, cancellation, recovery, and terminal outcome.

The WebSocket/SSE/REST mechanism used to deliver them is not event authority.
Clients can resume from sequence and compare their view with durable storage.

## Development acceptance evidence

Historical trains retain their candidate and completion receipts. From the
v0.7 product-first train onward, acceptance is organized once per Epic: a real
target end-to-end journey plus `make test` and `make lint`; release-wide
`make check-contract` and signed platform artifacts run once before release.
Do not invent new story-level receipts for current work.

Evidence names source commits, tests, environment dimensions, target calls,
secret findings, and residue. Failed evidence remains history; it is not
deleted when a repair passes. The v0.7 P0-P5 journeys passed at
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac`; its signed build receipt has
`local-acceptance` scope and is not an official release record.

## Evidence classes

| Class | What it can prove |
|---|---|
| static | Types, schemas, build, unit/fuzz/golden contracts |
| db | Behavior against the real supported metadata database |
| lab | Real Patroni, etcd, PostgreSQL, Pigsty, or Site Agent behavior |
| browser | User-visible and accessibility behavior in the pinned browser |
| remote-ci | A named remote run URL and exact commit |

Static or mock evidence cannot stand in for a required real environment.

## Incident preservation

Before cleanup, preserve the immutable plan, approvals, Operation/Step/Event
records, three result axes, driver evidence, Site Agent journal records, and
target observations. Hash exported evidence and record who collected it.
