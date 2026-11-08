---
title: 'DN-013：复用结构，不泄露权威'
description: Boar 从 Bytebase 学到了什么，又明确拒绝了哪些产品模型与前端技术。
date: 2026-02-13
lastmod: 2026-09-08
weight: 130
categories: [工程]
tags: [bytebase, 复用, 脚手架, 迁移]
---

## 背景

Boar 早期评估 Bytebase 作为成熟 Go Application Scaffolding 来源。正确的问题不是“如何
移植 Bytebase”，而是“哪些基础设施模式独立于 Bytebase 的产品模型”。

## 采用的模式

Boar 有意只 Adapt 一小组内容：

- Thin Executable Entry 与 Cobra Root Lifecycle；
- 通过 Linker Flag 注入 Version；
- 通过 Build Tag 区分 Development/Release Profile；
- Server init → run → graceful shutdown 结构；
- Echo Middleware 与 Route Organization；
- 内嵌生产 SPA；开发时由 Vite 在 5173 端口提供 SPA，并默认把 `/api` 代理到 9876 端口的
  Go Server；
- 由 PostgreSQL Advisory Lock 保护的 Embedded Sequential Migration；
- 独立 Database Connection Layer；
- 先 Frontend、后 Embedded Binary 的两阶段构建。

每个模式都翻译为 Boar 的命名、依赖与 Failure Semantics，而不是作为永久外来抽象复制。

开发拓扑需要精确说明：未带 `embed_frontend` 的 Go Build 不会反向代理 Vite；它只提供 API
和一个说明「Frontend 未内嵌」的信息页。开发时由 Vite Process 接受 Browser Traffic，并把
API Request 代理给 Go。Release Build 先生成 `frontend/dist`，复制到
`internal/server/dist`，再用 `release,embed_frontend` 编译 Go Binary。

## 明确拒绝

Boar 没有搬运 Bytebase 的 Vue Frontend、Pinia Store、Naive UI Component 或产品业务逻辑。
Boar UI 使用 React、Zustand、React Query 与项目 Design System。更重要的是，数据库管理
Authority 不会从另一个产品的 Workflow Model 继承。

## 规则

复用在基础设施边界停止。借来的 Server Lifecycle 不能决定 Boar 的 Resource Identity、
Risk、Approval、UNKNOWN 或 Audit Semantics。

同一原则也适用于 Provider Library 与 Theme：采用已经验证的机制，但把 Authority 保留在
Boar Versioned Contract 中。

## 为什么要记录

脚手架一旦稳定就会变得不可见。同时记录 Adopted 与 Rejected 内容，可以防止维护者无理由
重写稳定基础设施，也防止误以为 Boar 是 Donor Product 的下游 Fork。

## 当前仓库依据

- `cmd/boar/main.go` 与 `cmd/boar/cmd/root.go`：Executable 与 Cobra Server Lifecycle。
- `internal/server/embed_dev.go`、`internal/server/embed_frontend.go` 与
  `internal/server/routes.go`：精确的开发态与内嵌 Frontend 行为。
- `frontend/vite.config.ts`：Vite Port、Base Path 与 `/api` Proxy Target。
- `Makefile`：开发进程及先复制 Frontend、后 Embed 的 Release Build。
- `internal/migrate/` 与 `internal/store/`：Migration 与 PostgreSQL Connection Layer 实现。
- `frontend/package.json` 与 `frontend/src/`：React、Zustand、React Query 与项目自有 UI
  技术栈。
