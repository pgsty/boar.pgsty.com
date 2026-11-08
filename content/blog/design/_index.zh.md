---
title: 设计笔记
description: 已接受的产品合同、架构决策与实现理由。
weight: 20
icon: fa-solid fa-compass-drafting
blog_index: table
sidebar_expanded: true
---

这 15 篇笔记解释 Boar 的设计决策，是源码仓库资料的摘要，不新增合同，也不证明某项
功能已经交付。文章保留原始发布日期，后续校正记录在 `lastmod` 中；涉及设计与当前
实现差异的地方会明确区分，并列出依据文件。

当前范围的权威是 Boar 仓库中的
`_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`，以及 Charter 的
产品定义、CKR 和已接受的 ADR 修订。编号 PRD、原始架构与历史收据用于解释早期列车，
并保留其兼容性约束。

本站的[状态与路线图](/zh/docs/develop/roadmap/)汇总已验收旅程、开发中工作与发布边界。
类型合同、原型、本地验收通过的旅程和正式发布，是四种不同的结论。
