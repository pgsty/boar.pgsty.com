---
title: Compatibility matrix
description: Historical v0.2 boundaries, v0.7 local acceptance, and permanent regression promises.
weight: 50
---

Compatibility is explicit and evidence-backed. Versions outside a reviewed
boundary are *unverified*, not silently compatible.

## Release status on 2026-09-08

The locally inspected repository has no Git tags, and this audit did not
verify a public release. `v0.2.0` is the historical Fusion acceptance baseline
in `BOAR-CHARTER.md`; it is not evidence of a published tag. The v0.7 cockpit
train passed local acceptance at
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac`, including `make test`, `make
lint`, `make check-contract`, and reproducible builds for four platforms. Its
signature scope is `local-acceptance`, not an official release.

The current development checkout has advanced beyond that acceptance commit.
Only evidence tied to an exact source commit establishes its reviewed
boundary.

## Historical Fusion v0.2.0 acceptance matrix

| Component | Reviewed boundary |
|---|---|
| Boar | `v0.2.0`, public schema `v1alpha1` |
| Linux artifact | `amd64`, `arm64`, `CGO_ENABLED=0` |
| Build toolchain | Go `1.26.6`, Node.js `26.4.0` |
| Browser gate | Playwright `1.62.1`, Chromium `151.0.7922.34` |
| Metadata PostgreSQL | `18.4` (`180004`), database `boar` |
| Patroni | release `4.0.7`; source lane `4.1.0` at the pinned commit |
| etcd | `3.5.33`, `3.6.14`, `3.7.1` |
| Pigsty | the source commit pinned in `compatibility/pigsty-config-source.yaml` |

These pins describe the v0.2 acceptance evidence. They do not claim that a
`v0.2.0` Git tag or public artifact currently exists.

## v0.7 local-acceptance build matrix

| Platform | Build and verify | Runtime smoke |
|---|---|---|
| Linux `amd64` | passed | native on host `mx` |
| Linux `arm64` | passed | not run; no QEMU/binfmt environment was available |
| Darwin `arm64` | passed | native |
| Darwin `amd64` | passed | Rosetta emulation |

All four archives were built twice with byte-identical binaries, archives,
and SBOM results. This proves the recorded local acceptance only.

The v0.7 real-target journeys recorded PostgreSQL `18.6` for the local
metadata and direct PostgreSQL target. The Pigsty protection journey used
Pigsty `4.5`, PostgreSQL `18.6`, and pgBackRest `2.59.1`. These are exact
accepted environments, not a claim of compatibility with every release in
their major-version families.

## Permanent regression assets

Control Plane v2 preserves:

- seven public Go packages: `config`, `model`, `patroni`, `dcs`, `dcs/etcd3`, `postgres`, `control`;
- 19/19 flat Patroni CLI commands and their human/JSON/YAML semantics;
- v1alpha1 schemas, OpenAPI, manifests, and downstream consumers;
- Outcome, SendState, Verification, and UNKNOWN semantics;
- no automatic retry for ambiguous writes;
- forward-only migration and append-only audit behavior;
- Pigsty parsing, redaction, source digest, and argv/environment allowlists.

Legacy paths can be deprecated only after same-domain differential evidence
proves successor equivalence.

## Source pins

Machine authority lives in the `compatibility/` manifests. They pin source
bodies, module versions, approved deviations, schema hashes, and public
contracts. Prose cannot broaden those pins.

## Browser boundary

The v0.2 release gate covers English and Chinese desktop/mobile journeys in
Chromium. It does not imply Firefox or WebKit parity.

See [DN-010: Permanent compatibility contract](/blog/design/permanent-compatibility-contract/).
