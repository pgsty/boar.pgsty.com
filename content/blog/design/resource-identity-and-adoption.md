---
title: 'DN-002: Resource identity and adoption'
description: Why a connection is not an asset, and why import must stop at a candidate graph.
date: 2026-08-24
lastmod: 2026-09-08
weight: 20
categories: [Architecture]
tags: [resource, identity, discovery, adoption]
series: [Control Plane v2]
---

## Problem

PostgreSQL management tools often start with a DSN and quietly let that DSN
become the identity of “the database.” That works until service discovery,
failover, tunnels, shared endpoints, clones, or privilege limits appear.

Pigsty inventory creates a different trap: because it contains desired names
and addresses, parsing it can be mistaken for proof that those assets exist or
for authority to change them.

## Decision

Boar separates Resource identity from access paths and keeps four management
axes independent:

- Provenance: `manual`, `created`, `discovered`, or `imported` origin;
- ManagementMode: `unmanaged`, `observed`, `imported`, `managed`, or
  `fully_managed`;
- SourceOfTruth: the authority for the Resource's declared state;
- ManagedFields: bounded field ownership by manager and operation.

Adoption is a typed lifecycle purpose that can move eligible Resources to
`managed`; it is not a `ManagementMode` wire value.

Connection is an Access Path. It is not PostgreSQL Instance identity. A system
identifier establishes cluster lineage but does not by itself identify a
physical instance.

## Evidence-based matching

Discovery emits observations and identity evidence. The public identity
assessment uses four exact decisions: `matched`, `candidate`, `conflict`, and
`insufficient_evidence`. Evidence carries `observedAt`, source, strength, and a
digest rather than raw identity material. A lower-privilege scan can add facts
it knows, but cannot erase facts it lacks permission to observe.

This is why `unknown` and `insufficient_privilege` are separate Capability
support values. If “not observed” were translated into “absent,” every
restricted connection could cause false drift or unsafe cleanup.

## Candidate graph

Pigsty import follows analyze → Candidate Graph → match/probe → reviewed diff →
Plan and commit. Local bundle import separately analyzes a bundle into a
Candidate Graph, requires authenticated review, and applies a typed Medium-risk
metadata Plan. Credential material is omitted, imported Resources remain inert
until credentials are rebound and freshly probed, and Capability is recomputed
instead of trusting the source snapshot. Parsing does not mutate the target,
and an unreviewed candidate does not become a persisted Resource.

Adoption is also distinct from object creation. An existing Patroni cluster can
be discovered and then adopted through a metadata-only, no-target-write Plan.
The current importer requires reachable, explicitly bound Patroni REST member
endpoints and corroborates system-identifier and address evidence; it also
verifies DCS evidence when a DCS reader is configured, but DCS verification is
optional.

## Lifecycle verbs

The model freezes three separate actions:

- **Stop Managing** removes Boar's active management relationship while keeping
  the external target.
- **Delete Resource** removes a control-plane record according to retention
  policy.
- **Destroy Target** causes an external destructive side effect and carries its
  own risk.

The current action-risk registry assigns `resource.stop_managing` Low,
`resource.delete` High, and `resource.destroy_target` Critical.

A UI that labels all three “Delete” has already violated the contract.

## Consequence

Resources can reconcile facts from Direct PostgreSQL, Patroni, Pigsty, and Site
Agent without making any one provider string the asset identity. The price is a
more explicit model; the benefit is avoiding irreversible action against the
wrong database.

Operator reference: [Resources and identity](/docs/concepts/resources/).

## Sources

- `BOAR-CHARTER.md` (CKR-009 and CKR-011)
- `resource/types.go`
- `resource/identity.go`
- `internal/importer/pigsty/analyze.go`
- `internal/localmigration/types.go`
- `internal/localimportkernel/driver.go`
- `internal/importer/patroni/graph.go`, `internal/importer/patroni/observer.go`, and `internal/importer/patroni/projection.go`
- `plan/risk.go`
