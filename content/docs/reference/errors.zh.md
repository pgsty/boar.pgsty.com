---
title: 错误与结果语义
description: 读取结构化错误，绝不把不确定外部写入折叠成普通失败。
weight: 40
---

Boar 错误同时面向人和自动化。例如，Operation 合同把非法状态转换序列化为：

```json
{
  "code": "BOAR-OPERATION-002",
  "message": "illegal Operation transition",
  "detail": "[REDACTED]",
  "hint": "[REDACTED]",
  "path": "$.state"
}
```

Code 格式为 `BOAR-{MODULE}-{NNN}`。HTTP Status 是传输信息；Boar Code 与类型化 Result
才是语义合同。Operation 错误的序列化逻辑会主动脱敏 `detail` 和 `hint`，不能假设
这些字段含有未经筛选的内部诊断信息。

## 三条独立结果轴

每个写入结果分别回答：

| 轴 | 精确取值 | 含义 |
|---|---|---|
| Outcome | `SUCCEEDED`、`FAILED`、`UNKNOWN` | 业务结果 |
| SendState | `NOT_SENT`、`MAYBE_SENT`、`ACCEPTED`、`REJECTED` | 派发及 Provider 接受请求的证据 |
| Verification | `CONFIRMED`、`UNCONFIRMED` | 权威证据是否已确定结果 |

`ACCEPTED` 不证明成功，`CONFIRMED` 也可以与已确定的失败同时出现。这些枚举中没有
`SENT` 或 `CONTRADICTED`。

规范的不确定案例是：

```text
Outcome=UNKNOWN
SendState=MAYBE_SENT
Verification=UNCONFIRMED
```

它表示 Boar 无法证明外部副作用是否发生，绝不表示“可以安全重试”。必须先检查 Provider
状态与持久化 Operation/Audit Evidence。

UNKNOWN 也可以与 `NOT_SENT / UNCONFIRMED` 及 `uncertainty=CONCURRENT_CONFLICT`
同时出现：Compare-and-set 前置条件不再成立，原来的观测失去权威。UNKNOWN 不只表示
传输超时；进入终态的 Operation 记录不会为了重试重新打开。

## 常见分类

- `BOAR-AUTH-*`：Authentication、Session 或 Token Authority。
- `BOAR-RESOURCE-*`、`BOAR-IDENTITY-*`：Resource 非法或 Identity 未解析。
- `BOAR-CAPABILITY-*`、`BOAR-POLICY-*`：Action 不可用或 Admission 被拒。
- `BOAR-PLAN-*`、`BOAR-APPROVAL-*`：Plan/Approval 非法、过期或未授权。
- `BOAR-OPERATION-*`、`BOAR-WORKER-*`、`BOAR-STORE-*`：持久执行与完整性。
- `BOAR-CONNECTION-*`、`BOAR-CREDENTIAL-*`、`BOAR-DISCOVERY-*`：访问与观测。
- `BOAR-SITEAGENT-*`：Enrollment、Identity、Protocol 或 Journal 失败。

## Client 行为

Client 可以按合同重试读取。只有 Action Contract、Idempotency Key、Durable Record 与
Send State 共同证明安全时，才允许重试 Mutation。Timeout 或 HTTP Response 丢失本身绝不
授予写入重放权限。

设计理由见 [DN-005：UNKNOWN 是第一等结果](/zh/blog/design/unknown-is-a-first-class-result/)。

依据：Boar 源码仓库的 `control/types.go`、`operation/state.go` 与 `operation/error.go`。
