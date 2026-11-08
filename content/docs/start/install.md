---
title: Install Boar
description: Build the current source or verify an explicitly published release.
weight: 20
---

As of 2026-09-08, the locally inspected repository has no Git tags, and this
audit did not verify a public release. Fusion `v0.2.0` is the historical
acceptance baseline recorded by the Charter, not proof of a published tag.
The `v0.7.0` cockpit train passed local acceptance at source
commit `3094b048f6d3510f28688c1507acb9a2d5f6e0ac`, but its receipt explicitly
uses `signatureScope=local-acceptance` and is not an official release
signature.

For evaluation and development, build the reviewed source ref. For
production, install only a release that has actually been published through
the project's release process.

## Verify a published release

The release pipeline produces platform archives, a CycloneDX SBOM, a build
receipt, `SHA256SUMS`, its Ed25519 signature, and a release public key. The
v0.7 local-acceptance build proved reproducible archives for Linux and macOS on
`amd64` and `arm64`; that local staging directory is evidence, not a download
channel.

Obtain every file from the same release. Compare the public-key fingerprint
through an independent trusted channel before treating the bundled key as a
trust anchor.

```bash
openssl pkeyutl -verify -pubin -inkey RELEASE-PUBLIC-KEY.pem \
  -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig
sha256sum -c SHA256SUMS
```

When an official release exists, install exactly one matching platform
archive. Replace `VERSION` and `PLATFORM` with values from that release:

```bash
tar -xzf "boar-${VERSION}-${PLATFORM}.tar.gz"
sudo install -o root -g root -m 0555 \
  "boar-${VERSION}-${PLATFORM}/boar" /usr/local/bin/boar
/usr/local/bin/boar version
```

The version output must agree with the reviewed source commit in the build
receipt.

## Build from source

The current source tree and the v0.7 local-acceptance receipt use Go `1.26.6`
and Node.js `26.4.0`. Use the toolchain declared by the exact ref you build.
The companion documentation site's toolchain is independent of the Boar
binary.

```bash
make build
```

`make build` installs frontend dependencies, builds the frontend, and produces
`bin/boar` with the frontend embedded. Package downloads use the project proxy
settings in the Makefile. Release acceptance is wider than a successful local
compilation; do not label an ad-hoc binary or the v0.7 local-acceptance
artifacts as an official release.

## Before production

- Read the [compatibility matrix](../../reference/compatibility/).
- Create a dedicated `boar` metadata database and non-superuser owner.
- Store configuration as a canonical regular file owned by the service UID with mode `0600`.
- Keep credentials in approved secret mechanisms, not in the repository or shell history.
- Back up metadata before every forward-only migration.

See [install, upgrade, and recovery](../../admin/upgrade-recovery/) for the
production sequence.
