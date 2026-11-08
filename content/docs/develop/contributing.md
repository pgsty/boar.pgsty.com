---
title: Contributing
description: Follow the package boundaries, versioned contracts, and evidence expectations.
weight: 40
---

## Commits

Use Conventional Commits. Keep one change coherent. For v0.7+ product work,
get the Epic journey working before adding focused tests for that journey and
the kernel invariants it exercises.

## Go

- Preserve one-way dependencies: handler → service/engine → tool/store or kernel/driver.
- Keep `model/` and public contract packages free of application side effects.
- Use structured `log/slog`; do not add logging dependencies.
- Give exported structures both `json` and `db` tags where they cross storage and wire boundaries.
- Format errors as `BOAR-{MODULE}-{NNN}` with Code, Message, Detail, and Hint.
- Avoid interfaces until multiple real implementations justify them; the Store port is intentional because PostgreSQL and SQLite both implement it.

## TypeScript and React

- Keep TypeScript strict and public types explicit.
- Put every user-visible string in i18n resources.
- Use functional components and hooks.
- Use theme variables instead of hard-coded colors.
- Use Lucide icons at the project stroke width; do not use Unicode emoji as UI icons.
- Preserve basename routing, keyboard access, mobile behavior, the light-theme
  token system, and the reserved `data-mode` path for later dark mode work.

## Schemas and migrations

PostgreSQL constraints are the final validation layer. Migrations are
forward-only and serialized by advisory lock. The audit table remains
insert-only. Public machine contracts evolve through versioned successors,
never silent in-place edits.

## Design changes

If a change affects a frozen control-plane axiom, CKR, risk mapping, or
compatibility promise, write an ADR or Correct Course and update traceability.
Current Epic scope is maintained in the v0.7–v1.0 roadmap.

## Pull request evidence

For an Epic exit, name the exact source, commands, real target, journey result,
`make test` and `make lint` result, and cleanup. Do not claim a real-system
result from static tests. Run the complete contract check once for the release,
and preserve failed-and-repaired history when it explains the final contract.
