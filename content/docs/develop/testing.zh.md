---
title: 构建与测试
description: 运行与风险相称的门禁，不把本地检查混同为真实环境证据。
weight: 30
---

## 工具链

- Go Module 基线：Go `1.26.6`。
- 前端：Node.js `26.4.0`、React `19.2.0`、TypeScript `5.9.3`、Vite `8.2.1`。
- 浏览器门：Playwright `1.62.1`、Chromium `151.0.7922.34`。
- 历史合同元数据基线：PostgreSQL `18.4`，数据库名 `boar`。v0.7 的 P0/P2/P4
  真实目标旅程使用 PostgreSQL `18.6`。

文档站使用相互独立的工具链：Hugo Extended `0.168.0`、Go `1.27.3` 与 Oink `v1.5.0`。

## 日常目标

```bash
make dev
make build
make test
make lint
```

`make test` 覆盖 Go 与 Frontend Suite；`make lint` 运行 Go 与 Frontend Check；
`make build` 生成内嵌前端的二进制。

## 发布与兼容门禁

```bash
make check-contracts
make check-contract
make test-public-core
make test-public-contracts
```

这些是保留的兼容与发布检查，不属于日常门禁。每趟发布只统一运行一次完整
`make check-contract`。它在永久历史门上增加 Charter Checker，并校验保留的 Receipt、
Manifest、Schema Inventory 与冻结资产。较小的 Public Core/Contract Target 继续用于
定向兼容工作。

## 真实环境

v0.7 起，每个 Epic 以一条面向真实目标的端到端旅程，加全绿 `make test` 与
`make lint` 关闭。例如 Patroni/etcd Integration、Pigsty Isolated Lab、PostgreSQL Direct
Connection、SQLite Store Parity、Site Agent Network Partition 与 Console Browser Journey。

不能用 Mock 替代要求的 Lab，也不能用 Component Snapshot 替代 Browser Journey。旅程跑通
后再补覆盖旅程与内核不变量的测试，新增测试行数不超过新增产品行数的三分之一。历史
Story Evidence 继续保留，新工作不再增加按 Story 的 Receipt 与 Checker。

## 数据库范围

本地开发只允许使用名为 `boar` 的 PostgreSQL Database。绝不能在同一 Cluster 的其他数据库
上运行 Test 或 Migration。创建 Schema、Role、Process、Socket 或 Container 的测试必须
证明 Cleanup 与零未知 Residue。

## 网络下载

仓库策略要求 `go mod download`、`go get`、`npm install`、`npx`、`pnpm install` 与其他
包下载使用指定 HTTP Proxy。
