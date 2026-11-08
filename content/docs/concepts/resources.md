---
title: Resources and identity
description: Model managed objects without confusing access paths, evidence, and ownership.
weight: 10
---

A Resource is Boar's versioned envelope for something the control plane can
observe or manage. It carries a kind, stable identity, desired and observed
facts, provenance, management state, relationships, and field ownership.

## Current resource kinds

The current `resource/v1` registry contains Workspace, Fleet, Site, Node,
Service, Connection, CredentialRef, PostgreSQLCluster, PostgreSQLInstance,
Endpoint, Database, Role, Extension, BackupRepository, and Backup. Plans and
Operations refer to Resources but are separate kernel records. Patroni and
Pigsty are represented through these resources, relationships, provenance, and
driver evidence rather than by loosening a generic provider object. Exact
schemas are versioned; adding a kind does not loosen an existing kind's
decoder.

## Connection is not identity

A connection URL, service entry, tunnel, or Site Agent path is an *access
path*. Several paths may reach the same asset, and one path may later resolve
to a different endpoint. Boar therefore keeps Connection separate from
PostgreSQL Instance and Asset identity.

Likewise, a PostgreSQL system identifier is strong cluster-lineage evidence,
but cannot alone establish physical-instance identity.

## Four independent axes

Do not collapse these fields into one provider label:

| Axis | Question |
|---|---|
| Provenance | Where did this fact or object come from? |
| Management mode | Is Boar observing, adopting, or actively managing it? |
| Source of truth | Which authority owns the declared fact? |
| Managed fields | Which actor owns each field? |

Because these axes are independent, an object may be discovered from Pigsty,
observed through a direct connection, and only partially managed by Boar.

This is visible in the accepted v0.7 journeys: an inventory member that has not
been imported as a Resource stays UNKNOWN even if a lifecycle job succeeded,
and an authorized Direct observation may be compared with Pigsty desired state
without transferring field ownership.

## Candidate graph and adoption

An import first creates a candidate graph. Identity matching classifies
evidence and conflicts before any object becomes managed. Adoption is an
explicit plan; `Stop Managing`, `Delete Resource`, and `Destroy Target` are
three different actions with different side effects.

## Unknown is information

Discovery failure never proves absence. A field that cannot be observed due to
insufficient privilege is recorded as `unknown/insufficient_privilege`. This
prevents low-privilege discovery from deleting or disabling facts it cannot
see.

See [DN-002: Resource identity and adoption](/blog/design/resource-identity-and-adoption/).
