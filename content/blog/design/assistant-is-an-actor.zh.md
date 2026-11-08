---
title: 'DN-008：Assistant 是 Actor'
description: 通过拒绝独立执行与审批权威，让 AI 保持真正有用。
date: 2026-08-24
lastmod: 2026-09-08
weight: 80
categories: [安全]
tags: [assistant, ai, mcp, 工具, prompt-injection]
series: [Control Plane v2]
---

## 决策

Boar 保留 DiagnosticEngine、Session State Machine、FastPath 与 AgentBridge，作为 Console
Assistant Feature。Assistant 不是系统核心；它提出的所有副作用都必须从 Human、API、
CLI 与 MCP 共用的 Kernel Plan 出口离开。

## 权威模型

Charter 定义了以下能力词汇，其中包含未来等级；它不是当前模型可调用的工具清单：

```text
ai.read
ai.explain
ai.diagnose
ai.plan
ai.request_approval
ai.apply_approved
ai.auto_remediate_low
```

它们不是 L1–L5 Safety Level，也不隐含 Human Role。Assistant 尤其没有 Raw Shell、Raw SQL
Write、Approve、Force 或 Arbitrary Tool Registration Authority。

AI Principal 与 Approver Principal 分离。受控 Assistant Facade 可以请求审阅、应用已经
审批的精确 Plan Hash，但当前两个描述符都标记为 `modelCallable=false`，模型不能调用。
`ai.auto_remediate_low` 不在当前工具清单中。Assistant 不能审批自己的 Plan，也不能在
审批后修改 Plan。

## 不可信输入

Database Comment、SQL、Log、Inventory、README、Alert、Provider Error 与检索到的文档全部
视为 Untrusted Data，其中可能包含意图影响模型的指令。

Closed-schema Tool 让这些指令保持为数据，而不是 Authority。Tool Selection 受 Effective
Capability 限制，Argument 经过类型校验。Human/Service Approval 验证 Principal Identity
与 Plan Hash，永远不把模型文字当作授权。

## MCP 边界

当前 MCP Inventory 精确暴露八个 Model-callable Tool：`resources.list`、
`resources.get`、`topology.get`、`metrics.query`、`logs.query`、`diagnose`、
`plan.create` 与 `plan.explain`，不暴露 Raw Write、Approval、Force 或 Apply Tool。

范围更宽的已认证 Assistant Facade 还描述 `plan.request_approval` 与
`plan.apply_approved`，但两者当前都是 `modelCallable=false`。请求审阅不会记录审批决定；
Apply 只接受已经审批的精确 Immutable Plan Hash，并委托 Kernel 路径执行。P10 计划把这两项
受治理操作加入 MCP，但不会把审批权交给模型。通用 Execution Tool 仍会违反产品合同。

## 保留既有用户价值

重新确立产品中心不等于删除 Assistant。既有 Session、七种 Block Renderer、版本化
WebSocket Envelope、Replay、Diagnostic Card 与 LLM Graceful Degradation 都保留。改变的
是所有权：Assistant Output 可以形成意图，但只有 Kernel 持有 Mutation。

## 为什么这更 AI-Native

AI-Native 不是给模型最多权限，而是让模型的每项贡献都有类型、可归因、可审查、可恢复，
并能由其他 Actor 等价替代。Authority 不存在于模型文本中，才能在替换或升级模型时保持
控制面安全合同不变。

## 当前仓库依据

- `BOAR-CHARTER.md`：产品身份、CKR 权威边界与 `ai.*` Capability 词汇。
- `internal/assistantmcp/contracts.go` 与
  `schema/assistantmcp/v1/inventory.schema.json`：Assistant/MCP 精确清单、封闭参数 Schema
  与 `modelCallable` 值。
- `internal/server/assistant_mcp.go` 与 `internal/handler/routes.go`：已认证 Facade 及其
  Kernel 委托路径。
- `_bmad-output/planning-artifacts/control-plane-roadmap-v0.7-v1.0.md`：P10 中两项未来
  MCP 操作的范围。
