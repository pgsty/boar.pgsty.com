---
title: 能力
description: 解释目标支持什么、Principal 可以做什么，以及原因。
weight: 20
---

Capability 是已发现事实与可用动作之间的合同。Console 不能通过判断 Provider 字符串来
决定是否显示某个动作。

## Intrinsic 与 Effective

- **Intrinsic Capability** 描述 Resource 与 Driver 原则上能做什么。例如 Patroni
  Cluster 支持 Switchover，PostgreSQL Target 提供动态参数元数据。
- **Effective Capability** 在综合 Access Reachability、Credential、Resource State、
  Policy、Risk、License Boundary、Principal Scope 与 Freshness 后给出最终结论。

Effective Record 包含显式 Decision 与 Reasons。仅把按钮置灰不够；Operator 必须知道
阻塞来自缺少 Credential、Discovery 过期、权限不足、Resource Lock 还是需要审批。

Feature Lane 配置只是一个输入。当前 Server Mode 的三条 Kernel 写通道默认开启，但动作
只有在 Policy 与当前证据参与计算后得到肯定的 Effective Capability 才可使用。Feature
Flag 永远不会直接授予 Principal 权威。

## 评估输入

```text
Resource Facts
+ Relationship Context
+ Driver Declaration
+ Connection and Credential State
+ Principal Scope
+ Policy and Risk
+ Freshness and Locks
= 带原因的 Effective Capability
```

Unknown 输入必须保留。例如，无法完成权限探测既不能视作明确拒绝，也不能视作明确授权。

## 稳定动作身份

Capability 引用版本化 Action Identity，而不是任意命令。Action Registry 把每个 Action
绑定到类型化输入、风险级别、Driver 支持与 Verification 行为。Driver 不能用声明降低
Kernel Registry 的风险定级。

## 用户界面规则

API、CLI、Console、MCP 与 Assistant 必须使用同一个 Effective Capability Decision。
界面表达可以不同，但执行权威不能不同。

v0.7 旅程已经本地验收读侧 Capability Reason 与 Low 风险 Session Cancel 路径。正在开发
的 v0.8 源码中出现的 Capability，只有通过相应 Epic 与列车旅程后才是已验收产品能力。

设计理由见 [DN-003：使用 Capability，而非 Provider Flag](/zh/blog/design/capability-not-provider-flags/)。
