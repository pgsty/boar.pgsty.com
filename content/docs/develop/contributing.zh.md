---
title: 参与贡献
description: 遵守 Package 边界、版本化合同与证据要求。
weight: 40
---

## Commit

使用 Conventional Commits，一次变更保持逻辑完整。v0.7 起的产品工作先跑通 Epic
Journey，再为该旅程及其涉及的内核不变量补写聚焦测试。

## Go

- 保持单向依赖：handler → service/engine → tool/store 或 kernel/driver。
- `model/` 与公共合同 Package 不包含应用副作用。
- 使用结构化 `log/slog`，不引入额外日志依赖。
- 跨 Storage 与 Wire 边界的导出 Struct 同时声明 `json` 与 `db` Tag。
- Error 格式为 `BOAR-{MODULE}-{NNN}`，包含 Code、Message、Detail 与 Hint。
- 没有多个真实实现时不要滥用 Interface；Store Port 因 PostgreSQL 与 SQLite 都要实现而
  属于有意抽象。

## TypeScript 与 React

- 保持 TypeScript Strict，公共类型显式。
- 所有用户可见文字进入 i18n Resource。
- 使用函数组件与 Hook。
- 使用 Theme Variable，禁止硬编码颜色。
- 使用项目规定 Stroke Width 的 Lucide Icon，禁止 Unicode Emoji 充当 UI Icon。
- 保持 Basename Routing、Keyboard Access、Mobile Behavior、亮色 Token System，以及为后续
  Dark Mode 预留的 `data-mode` 路径。

## Schema 与 Migration

PostgreSQL Constraint 是最终校验层。Migration 只向前，并由 Advisory Lock 串行执行。
Audit Table 保持 Insert-only。公共 Machine Contract 通过版本化 Successor 演进，不能
静默就地改写。

## 设计变更

如果变更影响冻结 Control-plane Axiom、CKR、Risk Mapping 或 Compatibility Promise，
必须编写 ADR/Correct Course 并更新 Traceability。当前 Epic 范围在 v0.7–v1.0 路线图中维护。

## Pull Request 证据

Epic 退出记录应注明精确 Source、Command、真实目标、Journey Result、`make test`、
`make lint` 与 Cleanup。不能从 Static Test 宣称 Real-system Result。完整 Contract Check
每趟发布只运行一次；若 Failed-and-repaired 历史对最终合同有实质解释作用，应予保留。
