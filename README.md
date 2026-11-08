# Boar Documentation

The bilingual documentation and engineering blog for the
[Boar PostgreSQL Control Plane](https://github.com/pgsty/boar).

## Documentation scope

Last fact check: **2026-09-08**, against the companion `../boar` source tree.
The [current status and roadmap](content/docs/develop/roadmap.md) distinguishes
the locally accepted v0.7 cockpit from ongoing v0.8 development and later plans.
Local acceptance and signed staging artifacts do not establish a public release.

When updating product claims, check the implementation and these source records:

- `../boar/_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`
  for the current delivery scope and acceptance rules.
- `../boar/BOAR-CHARTER.md` for the product definition, CKR invariants, and
  OSS/Enterprise boundary; its original train schedule is historical.
- `../boar/docs/acceptance/v0.7/README.md` and
  `../boar/docs/acceptance/v0.7/release/release-summary.json` for completed
  journeys, artifact identity, and verification limits. The accepted v0.7 source
  is `3094b048f6d3510f28688c1507acb9a2d5f6e0ac`.
- `../boar/cmd/boar/cmd/`, `internal/config/`, and `internal/handler/routes.go`
  for actual commands, defaults, and endpoints.

Maintain English and Chinese together. Keep historical design and release notes
dated, and link them to the current roadmap when their plans have been superseded.
`make check` validates the build, language pairs, untranslated Chinese in English
sources, outputs, and internal links including same-page anchors. It does not
prove product functionality or publication of release artifacts.

## Toolchain

- Hugo Extended `0.168.0`
- Go `1.27.3`
- Oink `v1.5.1`

## Local preview

```bash
export HTTP_PROXY=http://127.0.0.1:8888
export HTTPS_PROXY=http://127.0.0.1:8888
export ALL_PROXY=http://127.0.0.1:8888
go mod download
make serve
```

The English site is served at `/`; Simplified Chinese is served at `/zh/`.

## Production build

```bash
make check
```

The static site is written to `public/`. Documentation is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code in this
repository is licensed under Apache License 2.0.

Local theme regression preview: run `make dev` with the sibling `../oink` checkout, or set `THEME_DIR=/path/to/oink`. This disables both Go and Hugo workspaces and uses the current local theme; the published module pin is unchanged.
