---
title: 'DN-013: Reuse structure, not authority'
description: What Boar learned from Bytebase without importing its product model or frontend stack.
date: 2026-02-13
lastmod: 2026-09-08
weight: 130
categories: [Engineering]
tags: [bytebase, reuse, scaffolding, migration]
---

## Context

Early Boar development evaluated Bytebase as a source of mature Go application
scaffolding. The useful question was not “how do we transplant Bytebase?” but
“which infrastructure patterns are independent of Bytebase's product model?”

## Adopted patterns

Boar adapted a deliberately narrow set:

- a thin executable entry point and Cobra root lifecycle;
- version injection through linker flags;
- development and release profiles through build tags;
- server init → run → graceful shutdown structure;
- Echo middleware and route organization;
- embedded production SPA, while Vite serves the development SPA on port 5173
  and proxies `/api` to the Go server on port 9876 by default;
- embedded, sequential migrations guarded by PostgreSQL advisory lock;
- a dedicated database connection layer;
- a two-stage frontend-then-embedded-binary build.

Each pattern was translated into Boar naming, dependencies, and failure
semantics rather than copied as a permanent foreign abstraction.

The development topology deserves precision: a non-`embed_frontend` Go build
does not reverse-proxy Vite. It serves the API and a small information page
saying that frontend assets are absent. The Vite process owns browser traffic
during development and proxies API requests to Go. Release builds first create
`frontend/dist`, copy it into `internal/server/dist`, then compile the Go binary
with `release,embed_frontend`.

## Explicitly rejected

Boar did not import Bytebase's Vue frontend, Pinia stores, Naive UI components,
or product business logic. Boar's UI uses React, Zustand, React Query, and the
project design system. More importantly, database-management authority was not
inherited from another product's workflow model.

## Rule

Reuse stops at the infrastructure boundary. A borrowed server lifecycle cannot
decide Boar's Resource identity, risk, approval, UNKNOWN, or audit semantics.

The same rule now applies to provider libraries and themes: adopt proven
mechanics, but keep authority in Boar's versioned contracts.

## Why record this

Scaffolding decisions become invisible once they work. Recording both the
adopted and rejected pieces prevents future maintainers from either rewriting
stable infrastructure without reason or assuming Boar is a downstream fork of
the donor product.

## Sources in the current repository

- `cmd/boar/main.go` and `cmd/boar/cmd/root.go` — executable and Cobra server
  lifecycle.
- `internal/server/embed_dev.go`, `internal/server/embed_frontend.go`, and
  `internal/server/routes.go` — the exact development and embedded frontend
  behavior.
- `frontend/vite.config.ts` — Vite port, base path, and `/api` proxy target.
- `Makefile` — development process and the frontend-copy-embed release build.
- `internal/migrate/` and `internal/store/` — migration and PostgreSQL
  connection-layer implementations.
- `frontend/package.json` and `frontend/src/` — React, Zustand, React Query, and
  the project-owned UI stack.
