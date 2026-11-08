---
title: 'DN-014: Offline license trust model'
description: Separate public-key verification, optional issuing, durable state, and product gating.
date: 2026-02-13
lastmod: 2026-09-08
weight: 140
categories: [Security]
tags: [license, jwt, es256, keys]
---

## Decision

Boar licenses are ES256 JWTs verified locally. Validation performs no network
request: it uses an embedded public key plus any configured verification keys.
Issuing is optional and exists only when a private key is configured and its
public half matches one of the verifier's keys.

## Claims

The validator accepts the Pig-compatible subject form
`type=<license_type>,node=<node_limit>` and explicit `license_type` /
`node_limit` fields. The fallback is pairwise in the current code: only when
`license_type` is empty does it parse the subject and assign both type and node
limit. If `license_type` is already present, the subject is not consulted and
`node_limit` keeps its explicit or zero JSON value.

Tokens require ES256 plus `exp`, `iat`, and `nbf`. Validation uses UTC wall time
and a 30-second leeway. `iss` and `aud` must each be non-empty, but the validator
does not compare either value with a configured allowlist. Negative node limits
are rejected after the subject fallback has produced the effective value.
Issued tokens include a random `jti`; validation does not require or revoke by
`jti`.

## Key separation

Verification keys are the embedded default plus configured public-key PEM text
or file paths. A private key is never necessary to verify or activate a
license.

The license PEM loader accepts inline PEM or calls `os.ReadFile` on the supplied
path. It does not perform the owner, mode, or symlink checks used by some other
credential-key loaders in Boar. Deployment file protection therefore remains
outside the guarantees of this license loader.

The optional issue endpoint is unavailable when no private key exists. When a
private key is configured, startup checks that its public half belongs to the
verification set, and the server immediately verifies every token it issues.
For this endpoint, `month=0` means an `exp` of 2200-12-31; it is still an
ordinary expiry claim, not a special non-expiring JWT type.

This removes a recurring ambiguity: “private-key injection” belongs to issuing;
verification always uses public keys.

## Durable state

The singleton PostgreSQL `license_state` record stores trial, active, expired,
or inactive state; type; node limit; expiry; trial window; normalized claims;
and update time. A missing record creates and persists a seven-day trial. The
raw license token and signing private key are not stored in that row.

Status requires authentication. Activation and issuing additionally require
the legacy `manage_access` permission (granted to `admin` and
`workspace_admin`) and are rate-limited. Their handlers call
audit insertion helpers, but an audit-insert failure is logged and does not
roll back an otherwise successful request. The issue endpoint is an
administrative/script surface rather than a default end-user UI.

`node_limit`, `features`, and normalized claims are currently parsed or stored;
the license service does not enforce node counts or feature names from those
claims. Current `expired`/`inactive` evaluation restricts only the optional
`session_message_write` path.

## Time and revocation limits

“Offline” describes local signature and time-claim verification. The current
implementation has no online entitlement lookup, revocation list, trusted-time
service, monotonic-clock journal, or general anti-rollback check. Token and
trial expiry depend on the host wall clock; persisted `expired` state remains
expired, but this is not a complete defense against clock rollback. Activation
also does not compare a valid token with the previously stored token to prevent
installing an older still-valid license.

The ES256 license signature is separate from release evidence. The v0.7 local
acceptance artifacts sign `SHA256SUMS` with Ed25519 and declare
`signatureScope=local-acceptance`; that does not sign the source tree, confer a
public release identity, or change license validation.

## Product-boundary correction

The implementation originally gated write features around license state. The
Control Plane v2 charter narrows what licensing may control to organizational
complexity and compliance features. Core reliability, safe recovery,
rejection, cancellation, and OSS control remain available after expiry.

That change does not invalidate the JWT trust model. It changes the allowed
consumers of license state.

Administrator reference: [Licensing and editions](/docs/admin/licensing/).

## Sources

- Claims, pairwise subject fallback, and PEM loading boundary: `internal/license/claims.go`, `internal/license/validator.go`.
- Issuance dates and `jti`: `internal/license/issuer.go`.
- Trial, expiry, cache, and current restriction consumer: `internal/license/service.go`, `internal/license/cache.go`.
- Durable row: `internal/migrate/migrations/0005_add_license_state.sql`, `internal/store/license.go`.
- Startup key matching, endpoint auth, rate limits, and audit behavior: `internal/server/server.go`, `internal/handler/routes.go`, `internal/handler/license.go`.
- Product boundary: `BOAR-CHARTER.md` (CKR-016, CKR-017, §7).
- Separate v0.7 artifact signature scope: `docs/acceptance/v0.7/README.md`, `docs/acceptance/v0.7/release/boar-v0.7.0-build-receipt.json`.
