---
title: 兼容矩阵
description: 历史 v0.2 边界、v0.7 本地验收与永久回归承诺。
weight: 50
---

兼容性必须显式且有证据支持。落在已审查边界之外的版本是“未经验证”，不是“默认兼容”。

## 2026-09-08 发布状态

本次本地检查的仓库没有 Git Tag，本次核对也没有验证任何公开 Release。`v0.2.0` 是
`BOAR-CHARTER.md` 中的历史 Fusion 验收基线，不能用来证明存在已发布 Tag。v0.7 驾驶舱
列车在提交
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac` 上通过了本地验收，包括 `make test`、
`make lint`、`make check-contract` 和四平台可重复构建；其签名范围是
`local-acceptance`，不是正式 Release。

当前开发 Checkout 已继续前进，超出该验收提交。只有绑定精确 Source Commit 的证据才能
建立对应审查边界。

## 历史 Fusion v0.2.0 验收矩阵

| 组件 | 已审查边界 |
|---|---|
| Boar | `v0.2.0`，公共 Schema `v1alpha1` |
| Linux 制品 | `amd64`、`arm64`、`CGO_ENABLED=0` |
| 构建工具链 | Go `1.26.6`、Node.js `26.4.0` |
| 浏览器门禁 | Playwright `1.62.1`、Chromium `151.0.7922.34` |
| 元数据 PostgreSQL | `18.4`（`180004`），数据库 `boar` |
| Patroni | Release `4.0.7`；固定提交上的 Source Lane `4.1.0` |
| etcd | `3.5.33`、`3.6.14`、`3.7.1` |
| Pigsty | `compatibility/pigsty-config-source.yaml` 固定的源码提交 |

这些 Pin 描述 v0.2 验收证据，不表示当前存在 `v0.2.0` Git Tag 或公开制品。

## v0.7 本地验收构建矩阵

| 平台 | 构建与验签 | 实际运行 |
|---|---|---|
| Linux `amd64` | 通过 | 在 `mx` 主机原生运行 |
| Linux `arm64` | 通过 | 未运行；当时没有 QEMU/binfmt 环境 |
| Darwin `arm64` | 通过 | 原生运行 |
| Darwin `amd64` | 通过 | Rosetta 模拟运行 |

四个平台均构建两次，二进制、归档与 SBOM 结果按字节一致。这只证明记录中的本地验收。

v0.7 真实目标 Journey 记录的本地元数据库与直连 PostgreSQL Target 均为 PostgreSQL
`18.6`。Pigsty Protection Journey 使用 Pigsty `4.5`、PostgreSQL `18.6` 与 pgBackRest
`2.59.1`。这些是精确的已验收环境，不代表同一主版本下的全部版本都已验证兼容。

## 永久回归资产

Control Plane v2 永久保留：

- 七个公共 Go Package：`config`、`model`、`patroni`、`dcs`、`dcs/etcd3`、`postgres`、`control`；
- 19/19 平铺 Patroni CLI 及 Human/JSON/YAML 语义；
- v1alpha1 Schema、OpenAPI、Manifest 与 Downstream Consumer；
- Outcome、SendState、Verification 与 UNKNOWN 语义；
- 模糊写入禁止自动重试；
- 前向 Migration 与仅追加 Audit；
- Pigsty Parse、Redaction、Source Digest 与 argv/environment Allowlist。

Legacy Path 只有在同域差分证据证明 Successor 等价后才能退役。

## Source Pin

机器权威位于 `compatibility/` Manifest，其中固定 Source Body、Module Version、Approved
Deviation、Schema Hash 与 Public Contract。文字文档不能扩大这些 Pin。

## 浏览器边界

v0.2 Release Gate 覆盖 Chromium 上的中英文 Desktop/Mobile Journey，不代表 Firefox 或
WebKit 已达成一致。

设计理由见 [DN-010：永久兼容合同](/zh/blog/design/permanent-compatibility-contract/)。
