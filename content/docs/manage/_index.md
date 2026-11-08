---
title: Manage PostgreSQL
description: Provider-specific workflows that preserve one control-plane contract.
weight: 30
icon: fa-solid fa-database
sidebar_expanded: true
---

Boar keeps provider-native semantics inside typed drivers and exposes one
resource-scoped workflow above them.

> [!NOTE]
> Status on 2026-09-08: the v0.7 P0-P5 journeys have passed local, real-target
> acceptance. The signed artifacts are local acceptance artifacts, not an
> official v0.7 release. v0.8 governance code is under development and has not
> passed Epic or release-train acceptance.

The accepted v0.7 Console includes the fleet overview and unified timeline,
Direct DBA read surfaces and session cancel, health reports, cluster protection,
and the Pigsty inventory/progress read surfaces. Each page keeps missing or
unproved facts UNKNOWN.

- [Direct PostgreSQL](direct-postgresql/) — inspect an arbitrary PostgreSQL URL with the accepted DBA read surfaces.
- [Patroni HA](patroni/) — preserve Patroni and DCS semantics with native 19-command compatibility.
- [Pigsty lifecycle](pigsty/) — inspect imported inventory and structured lifecycle evidence.
- [Local mode](local/) — run the single-user SQLite kernel within its accepted scope.
- [Site Agent](site-agent/) — establish outbound mTLS identity; general Plan dispatch remains v1.0 P14 work.
  {.cards}
