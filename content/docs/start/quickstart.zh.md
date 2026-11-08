---
title: 快速开始
description: 从源码运行 Boar，并验证第一条只读访问路径。
weight: 10
---

本页面面向本地开发工作站，对应 2026-09-08 的源码快照，不是生产部署指南。

## 前置条件

- 当前 Boar 源码树使用 Go `1.26.6`。
- React 前端使用 Node.js `26.4.0` 与 npm。
- Server Mode 需要 PostgreSQL 18，元数据库名称必须是 `boar`；v0.7 本地 Journey 实际使用 `18.6`。
- 已检出 `github.com/pgsty/boar` 源码。

> [!WARNING]
> 元数据库不是受管业务数据库。绝不能把 Boar 迁移指向存有业务数据的 PostgreSQL 数据库。

## 启动带 Console 的 Server Mode

最简单的开发路径会在 5173 端口启动 Vite，并在 9876 端口启动 Go Server：

```bash
make dev
```

打开 `http://127.0.0.1:5173/`。Vite 提供 React 应用，并把 `/api` 代理到
`127.0.0.1:9876` 后端。元数据库为空时，Boar 会跳转到 `/setup`。填写用户名、邮箱与密码
创建第一个管理员，然后在 `/login` 登录。系统没有默认管理员或默认管理员密码。

只显式启动后端时执行：

```bash
go run ./cmd/boar server \
  --database-url 'postgres:///boar?sslmode=disable' \
  --server-addr '127.0.0.1:9876'
```

非内嵌源码构建只提供 API 与后端说明页，不会提供或代理 React 应用；使用这条命令时还需
单独启动 Vite 并打开 5173 端口。裸 `boar` 当前会启动同一个 Server Runtime，但新脚本
应显式使用 `boar server`。

## 启动 Local Mode

Local Mode 需要内嵌前端二进制。先构建，再为独立 SQLite Kernel Store 提供绝对路径且
仅 Owner 可访问的状态目录：

```bash
install -d -m 0700 "$PWD/.local/boar"
make build
./bin/boar local \
  --state-dir "$PWD/.local/boar"
```

Local 默认使用 `--listen 127.0.0.1:0`，选择空闲端口并打开浏览器。无界面验证时使用
`--no-open-browser`；受保护的 `--bootstrap-file` 只有与 `--no-open-browser` 一起使用时
才会被接受。如果 Local Mode 试图绑定非回环地址，Boar 会直接拒绝，而不是静默暴露
单用户控制面。
`go run ./cmd/boar local` 属于非内嵌构建，会因为 Local Frontend 不可用而退出。

## 连接目标之前先验证

先读取进程健康与版本信息：

```bash
curl --fail --silent http://127.0.0.1:9876/api/v1/health
curl --fail --silent http://127.0.0.1:9876/api/v1/version
```

开发环境没有安装 Claude Code 时，Assistant 健康可能显示 degraded；元数据库健康与
类型化控制能力会独立呈现。

## 下一步

1. 选择生产拓扑前阅读[运行模式](../runtime-modes/)。
2. 检查[配置](../configuration/)，替换全部开发密钥。
3. 导入或连接目标前理解[资源与身份](../../concepts/resources/)。
4. 启用写入通道前阅读[安全模型](../../admin/security/)。
