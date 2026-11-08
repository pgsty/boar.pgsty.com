---
title: Licensing and editions
description: Understand ES256 license state without gating open-source reliability.
weight: 40
---

Boar retains its JWT-based license framework, but Control Plane v2 freezes a
clear product boundary: reliability and core control-plane safety remain open
source.

## License token

License tokens use ES256. Verification accepts configured public keys; optional
issuing requires a separate private key. The durable `license_state` record
stores activation state and token metadata, while raw private signing material
stays outside the database.

The API provides status, activation, and—only when an issuing key is
configured—issue flows. License changes are authenticated, authorized,
rate-limited, and audited.

The activation and issuance handlers attempt audit insertion, but currently
log an audit-insert failure without rolling back the request. This is not the
Kernel's atomic Operation/Event/Audit commit guarantee. Signature validation
also requires non-empty issuer and audience claims without matching them to a
configured identity allowlist; see the [offline license trust model](/blog/design/offline-license-trust-model/).

## OSS boundary

The Charter permanently assigns these capabilities to OSS. This is an edition
boundary, not a claim that every planned workflow is implemented:

- Local and Server modes;
- Resource, Capability, Planner, Operation, and Audit;
- core PostgreSQL, Patroni, Pigsty, PIG/SOW, and pgBackRest drivers;
- basic RBAC and approval;
- Site Agent;
- local accounts;
- MCP's eight model-callable read, diagnose, plan-create, and plan-explain tools.

Enterprise may add multi-organization isolation, SAML/SCIM, advanced OIDC,
high-availability control plane, external KMS/HSM, WORM/SIEM compliance,
multi-stage CAB, fleet federation, signed plugin certification, and commercial
support.

Those are permitted Enterprise areas, not a list of shipped integrations.
For current delivery limits, see [Status and roadmap](../../develop/roadmap/)
and the [Site Agent prototype](../../manage/site-agent/).

The Assistant facade also defines approval-request and apply-approved actions,
but both are `modelCallable=false`; the MCP model cannot approve or apply a
Plan.

## Reliability invariant

A license cannot disable safe recovery, rejection, cancellation, or the core
control plane. The kernel and public packages do not import License, Console,
LLM, Web, or legacy metadata dependencies. A legacy `control_write` feature
gate must not become a kill switch for OSS reliability.

In the current Server implementation, the initial trial lasts seven days.
Expired or inactive state restricts only `session_message_write`, enforced on
`POST /api/sessions/:sid/messages`. Core control writes, confirmation, and user
management are not included in `RestrictedFeatures`. This concrete behavior
should not be replaced with an assumed Enterprise feature matrix.

Expiry cannot make an already-running Operation unverifiable or impossible to
cancel safely. Local does not consume the Server's license gate.

See [DN-011: Open-source reliability boundary](/blog/design/oss-reliability-boundary/).

Source: `BOAR-CHARTER.md` §7, `internal/license/service.go`,
`internal/handler/routes.go`, and `internal/handler/middleware.go` in the Boar
repository.
