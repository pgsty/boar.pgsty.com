---
title: Security model
description: Protect credentials, separate principals, and make every external write auditable.
weight: 10
---

Boar's security model begins at the control-plane kernel. Authentication and UI
confirmation are necessary, but neither can compensate for an execution path
that bypasses Plan, Policy, Operation, or Audit.

## Trust boundaries

- **User and service principals** authenticate to Server and receive explicit
  workspace/resource scopes through RBAC and Policy.
- **Assistant principal** is separate from the approving principal. It has no
  raw shell, raw SQL write, approval, or force authority.
- **Site Agent identity** is established by approved enrollment and outbound
  mTLS, then bound to a site and typed action scope.
- **Provider credentials** are referenced or encrypted in dedicated credential
  storage and never copied into Resources, Plans, Events, Audit, prompts, or
  screenshots.
- **Release keys** and credential master keys are independent trust roots and
  must not be inferred from the artifact they verify.

## File and secret handling

Configuration, service files, passfiles, TLS private keys, control plan keys,
credential master keys, and signing keys must satisfy their exact contracts:
canonical regular files, no symlink traversal, expected owner, restrictive
mode, and bounded content.

Do not assume every key loader enforces identical checks. The current license
key helper accepts inline PEM or a file path and reads files without the
control/credential loaders' owner, mode, or symlink checks. Deployment must
protect that source; license key-pair matching does not enforce file permissions.

Direct request or prompt secrets are one-shot and non-joinable. System trust
roots and prompt/request material do not become reusable ambient caches across
trust changes.

## Transport

- Prefer PostgreSQL `VERIFY_FULL` / `sslmode=verify-full`.
- `VERIFY_CA`, encrypted-but-unverified, or plaintext access requires an
  explicitly approved deviation.
- PostgreSQL channel binding `REQUIRE` must negotiate
  `SCRAM-SHA-256-PLUS`.
- Endpoint selection remains separate from credentials; a service or
  environment host cannot silently replace the chosen Patroni member.
- Site Agent uses outbound mTLS and a pinned identity lifecycle.

## Mutation safety

Every mutation requires a fresh sealed Plan, effective capability, scoped
principal, policy admission, and durable Operation. Approval binds the full
plan digest. Operations commit ownership before external calls, and ambiguous
writes remain UNKNOWN without automatic retry.

`kernel_patroni_restart`, `kernel_patroni_domain`, and
`kernel_postgres_write` all default to `true`. They select the Kernel as the
write authority; they do not auto-approve a mutation. With Kernel control
enabled, legacy direct write commands are rejected in favor of the exact Plan,
approval, and admission path.

## Audit integrity

Audit is append-only. Production database privileges revoke update and delete
on audit rows. Operational events and provider evidence are preserved even
when execution fails or is rejected.

## Incident response

Stop new writes, isolate the exact target, revoke exposed credentials or keys,
and preserve binary/config hashes, Plan ID, Operation ID, Outcome, SendState,
Verification, Events, and Audit before cleanup. Follow the
[recovery runbook](../upgrade-recovery/) and reconcile every UNKNOWN result
against the provider before resuming.
