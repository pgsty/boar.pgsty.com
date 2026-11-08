---
title: Install, upgrade, and recovery
description: Verify artifacts, apply forward-only migrations, and recover without erasing evidence.
weight: 20
---

As of 2026-09-08, the locally inspected repository has no Git tags, and this
audit did not verify a public release. Fusion `v0.2.0` is a historical
acceptance baseline, and the v0.7 acceptance record says its signed artifacts
have `local-acceptance` scope rather than official release identity. This
runbook applies when operating an explicitly published release; always read
the release note for the exact target version.

## Before installation

Verify the release public-key fingerprint over an independent channel, then
verify the Ed25519-signed checksum file and every payload:

```bash
openssl pkeyutl -verify -pubin -inkey RELEASE-PUBLIC-KEY.pem \
  -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig
sha256sum -c SHA256SUMS
```

Confirm the version and reviewed 40-character source commit from the build
receipt after installation. Do not promote an ad-hoc source build or a local
acceptance artifact to production merely because its checksum is valid.

## Back up before upgrade

Stop new confirmed writes, wait for active Jobs and Operations to become
terminal, and record every unresolved UNKNOWN. Back up the exact metadata
database and migration ledger:

```bash
export BOAR_DATABASE_URL='postgres://boar_service@127.0.0.1:5432/boar?sslmode=verify-full'
pg_dump --format=custom --file=boar-before-upgrade.dump "$BOAR_DATABASE_URL"
psql "$BOAR_DATABASE_URL" -Atqc \
  "SELECT string_agg(version, ',' ORDER BY version) FROM schema_migrations" \
  > boar-before-upgrade.schema-migrations
```

Treat the dump as production data. It can contain users, audit evidence,
resource metadata, and credential locators.

The database dump does not contain the external authority needed to decrypt or
operate it. Back up the canonical configuration, `control_plan_key_file`, all
files named by `credential_master_key_files`, and the owner-private
`state_dir` that may contain the auto-provisioned `auto-v1` key. Preserve
ownership and file modes, and store this key material separately from the
database backup. Without the active and historical credential keys, restored
credential envelopes cannot be opened.

## Upgrade

1. Verify the new release and source commit.
2. Stop the old Boar process without deleting metadata.
3. Back up the exact `boar` database and its external configuration and key authorities.
4. Run `boar migrate` under its advisory lock.
5. Start the new binary with the same canonical configuration.
6. Verify version, migration ledger, health, pending approvals, active
   Operations, and unresolved UNKNOWN results.

```bash
/usr/local/bin/boar --database-url "$BOAR_DATABASE_URL" migrate
/usr/local/bin/boar server --config /etc/boar/boar.yml
```

Never run two different Boar versions against the database during migration.

## Rollback

Migrations are forward-only. Do not run an older binary against an advanced
database. Rollback requires a new empty `boar` database restored from the
pre-upgrade backup, then the previous reviewed binary.

Database replacement and restore are destructive production operations. Resolve
the exact target and obtain production approval before `dropdb`, `createdb`, or
`pg_restore --clean`.

## Recovery

1. Preserve binary hash, config hash, time, Plan/Operation/Job IDs, all three
   result axes, events, and audit rows.
2. For `UNKNOWN/MAYBE_SENT/UNCONFIRMED`, inspect Patroni, DCS, PostgreSQL,
   Pigsty, or the Site Agent journal before any retry.
3. If metadata is unavailable, stop writes and restore the last verified dump
   to a new database together with its matching configuration and key
   authorities.
4. If only the Assistant dependency is unavailable, typed control may continue
   read-only or degraded according to health and policy.
5. Reconcile active leases, locks, approvals, sessions, and terminal
   projections before reopening writes.
