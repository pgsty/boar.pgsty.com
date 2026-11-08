---
title: 安装、升级与恢复
description: 校验制品、应用前向迁移，并在不抹除证据的前提下恢复。
weight: 20
---

截至 2026-09-08，本次本地检查的仓库没有 Git Tag，本次核对也没有验证任何公开
Release。Fusion `v0.2.0` 是历史验收基线；v0.7 验收记录明确其签名制品只具有
`local-acceptance` Scope，不具备正式 Release Identity。本手册适用于实际明确发布的
版本；每次升级都必须阅读精确目标版本的 Release Note。

## 安装之前

先通过独立渠道核对 Release Public Key Fingerprint，再验证 Ed25519 签名的 Checksum
File 与全部 Payload：

```bash
openssl pkeyutl -verify -pubin -inkey RELEASE-PUBLIC-KEY.pem \
  -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig
sha256sum -c SHA256SUMS
```

安装后确认 Version，并与 Build Receipt 中经过审查的 40 位 Source Commit 一致。临时源码
构建或本地验收制品即使 Checksum 正确，也不能因此直接晋升为生产 Release。

## 升级前备份

停止新的已确认写入，等待 Active Job 与 Operation 进入终态，记录所有未解决 UNKNOWN。
备份精确元数据库与 Migration Ledger：

```bash
export BOAR_DATABASE_URL='postgres://boar_service@127.0.0.1:5432/boar?sslmode=verify-full'
pg_dump --format=custom --file=boar-before-upgrade.dump "$BOAR_DATABASE_URL"
psql "$BOAR_DATABASE_URL" -Atqc \
  "SELECT string_agg(version, ',' ORDER BY version) FROM schema_migrations" \
  > boar-before-upgrade.schema-migrations
```

备份属于生产数据，可能包含 User、Audit Evidence、Resource Metadata 与 Credential
Locator。

Database Dump 不包含解密与运行所需的外部权威。还必须备份规范 Configuration、
`control_plan_key_file`、`credential_master_key_files` 列出的全部文件，以及可能保存自动
创建 `auto-v1` Key 的 Owner-private `state_dir`。保留 Owner 与 File Mode，并把这些 Key
Material 与数据库备份分开保存。缺少当前或历史 Credential Key 时，恢复后的 Credential
Envelope 无法打开。

## 升级

1. 验证新 Release 与 Source Commit。
2. 停止旧 Boar Process，但不删除 Metadata。
3. 备份精确 `boar` 数据库及其外部 Configuration 与 Key Authority。
4. 在 Advisory Lock 下执行 `boar migrate`。
5. 使用同一份规范 Configuration 启动新 Binary。
6. 验证 Version、Migration Ledger、Health、Pending Approval、Active Operation 与所有
   未解决 UNKNOWN。

```bash
/usr/local/bin/boar --database-url "$BOAR_DATABASE_URL" migrate
/usr/local/bin/boar server --config /etc/boar/boar.yml
```

迁移期间绝不能让两个不同版本同时连接同一数据库。

## 回滚

Migration 只向前。不能让旧 Binary 连接已升级数据库。回滚必须创建新的空 `boar` 数据库，
恢复升级前备份，再启动上一个经过审查的 Binary。

Database Replacement 与 Restore 是破坏性生产操作。执行 `dropdb`、`createdb` 或
`pg_restore --clean` 前必须解析精确目标并取得生产审批。

## 恢复

1. 保存 Binary Hash、Config Hash、时间、Plan/Operation/Job ID、三条结果轴、Event 与
   Audit Row。
2. 遇到 `UNKNOWN/MAYBE_SENT/UNCONFIRMED` 时，重试前检查 Patroni、DCS、PostgreSQL、
   Pigsty 或 Site Agent Journal。
3. Metadata 不可用时停止写入，把最后一份已验证备份及匹配的 Configuration 与 Key
   Authority 恢复到新数据库。
4. 只有 Assistant 依赖不可用时，可按 Health 与 Policy 保持类型化 Control Read-only 或
   Degraded。
5. 重新开放写入前，对账 Active Lease、Lock、Approval、Session 与 Terminal Projection。
