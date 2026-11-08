---
title: 安装 Boar
description: 构建当前源码，或校验已经明确发布的正式制品。
weight: 20
---

截至 2026-09-08，本次本地检查的仓库没有 Git Tag，本次核对也没有验证任何公开
Release。Fusion `v0.2.0` 是 Charter 记录的历史验收基线，不能证明存在已发布 Tag。
`v0.7.0` 驾驶舱列车在源码提交
`3094b048f6d3510f28688c1507acb9a2d5f6e0ac` 上通过了本地验收，但 Receipt 明确标记
`signatureScope=local-acceptance`，不是正式发布签名。

评估与开发环境可以构建经过审查的源码 Ref。生产环境只应安装通过项目 Release 流程
实际发布的版本。

## 校验正式发布制品

Release Pipeline 会生成平台归档、CycloneDX SBOM、Build Receipt、`SHA256SUMS`、
Ed25519 签名与发布公钥。v0.7 本地验收已经证明 Linux 与 macOS 的 `amd64`、`arm64`
归档可重复构建；这些本地 Staging 文件是验收证据，不是下载渠道。

所有文件必须来自同一份 Release。只有通过独立可信渠道核对公钥指纹后，才能把随制品
分发的公钥视为 Trust Anchor。

```bash
openssl pkeyutl -verify -pubin -inkey RELEASE-PUBLIC-KEY.pem \
  -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig
sha256sum -c SHA256SUMS
```

正式 Release 存在时，只安装与目标平台一致的一份归档。请用该 Release 的实际值替换
`VERSION` 与 `PLATFORM`：

```bash
tar -xzf "boar-${VERSION}-${PLATFORM}.tar.gz"
sudo install -o root -g root -m 0555 \
  "boar-${VERSION}-${PLATFORM}/boar" /usr/local/bin/boar
/usr/local/bin/boar version
```

版本输出必须与 Build Receipt 中经过审查的源码提交一致。

## 从源码构建

当前源码树与 v0.7 本地验收 Receipt 使用 Go `1.26.6` 与 Node.js `26.4.0`。构建时应以
精确 Git Ref 声明的工具链为准；伴生文档站的工具链与 Boar 二进制相互独立。

```bash
make build
```

`make build` 安装前端依赖、构建前端，并生成内嵌前端的 `bin/boar`。下载依赖时 Makefile
使用项目代理设置。发布验收远不止“本地编译成功”，不要把临时构建或 v0.7 本地验收
制品标记成正式 Boar Release。

## 上生产之前

- 阅读[兼容矩阵](../../reference/compatibility/)。
- 创建专用 `boar` 元数据库及其非超级用户 Owner。
- 配置必须是 Service UID 所有、权限 `0600` 的规范普通文件。
- 凭据必须进入批准的 Secret 机制，不能进入仓库或 Shell History。
- 每次前向迁移前备份元数据。

完整生产顺序见[安装、升级与恢复](../../admin/upgrade-recovery/)。
