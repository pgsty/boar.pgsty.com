---
title: 'DN-011: The open-source reliability boundary'
description: License organizational complexity, never the safety required to control PostgreSQL.
date: 2026-08-24
lastmod: 2026-09-08
weight: 110
categories: [Product]
tags: [open-source, enterprise, license, reliability]
series: [Control Plane v2]
---

## Decision

Core reliability is permanently open source. A license may gate organizational
complexity and compliance integrations, but it cannot disable the mechanisms
that make PostgreSQL control safe.

## Frozen edition boundary

- Local and Server runtimes and Direct Connection;
- Resource, Capability, Planner, Operation, and Audit;
- core PostgreSQL, Patroni, Pigsty, PIG/SOW, and pgBackRest drivers;
- basic RBAC and approval;
- Site Agent and local accounts;
- MCP read and plan.

These are not a teaser tier. They are the product's required reliability
substrate under CKR-016 and ADR-011. The list fixes edition placement; it does
not assert that every roadmap journey around each component has shipped. For
example, the repository has a Site Agent prototype, while the complete
dispatch channel, air-gap/NAT journey, and generated clients remain P14–P15
work in the v1.0 roadmap.

## Enterprise may include

Multi-organization isolation, SAML/SCIM, advanced OIDC, HA control-plane
deployment, external KMS/HSM, WORM/SIEM integration, multi-stage CAB, fleet
federation, signed plugin certification, and commercial support belong to the
Enterprise boundary.

The distinction is organization and compliance scale—not whether an operator
can cancel a dangerous operation or inspect an audit trail.

## Current expiry behavior

License expiry must not break:

- safe recovery from a running or ambiguous Operation;
- rejection and policy enforcement;
- cancellation;
- core OSS control writes;
- verification and audit.

The migration away from the old `control_write` gate is present in current
code. For `expired` and `inactive`, `internal/license/service.go` reports only
`session_message_write` as restricted. Core confirmation, approval, rejection,
cancellation, user management, and control writes are not in that restriction
set; handler tests cover the recovery and core-approval cases.

That remaining restriction is the optional legacy Console Assistant message
write path. It is current implementation behavior, not evidence that all
Assistant functionality is an Enterprise product. Any future edition mapping
must still satisfy CKR-016's narrower rule: License may gate organizational
complexity and compliance capabilities only.

Kernel and public packages cannot import License, so a commercial decision
cannot become a hidden execution dependency.

## License framework remains useful

Boar keeps offline ES256 verification, optional local issuing, durable license
state, and an in-process evaluated-snapshot cache. Activation and issuing are
authenticated, require the legacy `manage_access` permission granted to
`admin` and `workspace_admin`, are rate-limited, and attempt audit inserts;
audit-insert failures are logged without rolling back a successful request.
Those mechanisms can express the Enterprise boundary cleanly. The
architectural constraint is what they are allowed to gate.

## Product consequence

The edition contract lets users evaluate and operate the real control plane in
OSS. Formal release status and roadmap completion are tracked separately; this
decision alone does not promote local acceptance artifacts into a public
release. Enterprise value belongs in larger organizational and compliance
surfaces rather than in the right to recover a database safely.

Administrator reference: [Licensing and editions](/docs/admin/licensing/).

## Sources

- Normative OSS/Enterprise boundary: `BOAR-CHARTER.md` (CKR-016, CKR-017, §7) and `_bmad-output/planning-artifacts/control-plane-decision-log.md` (ADR-011).
- Current restrictions and cache behavior: `internal/license/service.go`, `internal/license/cache.go`.
- Current route, RBAC, rate-limit, and audit wiring: `internal/handler/routes.go`, `internal/handler/license.go`, `internal/store/license.go`.
- Expired-license regression behavior: `internal/license/service_test.go`, `internal/handler/middleware_test.go`.
- Site Agent completion boundary: `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md` (P14–P15).
