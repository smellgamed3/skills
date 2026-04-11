---
name: outline-cli
description: 当需要通过命令行与 Outline（wiki 知识库）交互时使用，包括读取、搜索、列出文档集合和文档。兼容云端（app.getoutline.com）和私有部署实例。
---

# Outline CLI

## 概述

Outline 是一款现代 wiki 知识库应用，提供完善的 RPC 风格 API。本技能提供一个轻量 Python CLI 工具，通过 `uv run` 零安装直接调用 API。

**核心理念：** 一个脚本，零安装开销 —— `uv run` 在首次运行时自动处理依赖。

## 适用场景

```
需要与 Outline 知识库交互？
│
├─ 读取或查看内容？
│  ├─ 按 ID/URL 查单篇文档 → documents.info
│  └─ 浏览集合文档树   → collections.documents
│
├─ 搜索内容？
│  ├─ 全文搜索         → documents.search
│  └─ 仅搜索标题（更快）→ documents.search_titles
│
├─ 列出资源？
│  ├─ 所有集合         → collections.list
│  └─ 集合内文档       → documents.list
│
└─ 获取详细元数据？
   ├─ 集合详情         → collections.info
   └─ 按 shareId 查文档 → documents.info (shareId)
```

**适合以下情况：**
- 从命令行查找 Outline 知识库中的文档或集合
- 在脚本或工作流中自动化调用 Outline API
- 探索集合的文档树结构

**不适合以下情况：**
- 创建或修改文档（请使用 Outline 网页端或具有写权限的 API Token）
- 尚未配置 API Key 时

## 快速开始

### 第一步：创建配置文件

```bash
mkdir -p ~/.config
cat > ~/.config/outline.json << 'EOF'
{
  "base_url": "https://app.getoutline.com",
  "api_key": "ol_api_..."
}
EOF
```

私有部署实例将 `base_url` 改为自己的地址，例如 `https://wiki.example.com`。

### 第二步：获取脚本

将 [`scripts/outline.py`](scripts/outline.py) 保存到本地（`uv` 首次运行时自动安装依赖）：

```bash
# 直接运行（推荐）
uv run scripts/outline.py <接口名> '<JSON 参数>'
```

### 安装 uv（如未安装）

```bash
# 先下载，检查后再执行
curl -LsSf https://astral.sh/uv/install.sh -o uv-install.sh
# 检查 uv-install.sh 内容后执行
sh uv-install.sh
```

## 接口速查表

| 资源 | 接口 | 关键参数 |
|------|------|----------|
| **集合** | `collections.info` | `id` |
| | `collections.list` | `query`、`statusFilter`、分页参数 |
| | `collections.documents` | `id` |
| **文档** | `documents.info` | `id` 或 `shareId` |
| | `documents.list` | `collectionId`、`userId`、`statusFilter`、分页参数 |
| | `documents.search` | `query`、过滤条件、分页参数 |
| | `documents.search_titles` | `query`、过滤条件、分页参数 |

### 通用分页参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `limit` | 25 | 每页返回条数 |
| `offset` | 0 | 起始偏移量 |
| `sort` | 各接口不同 | 排序字段 |
| `direction` | `DESC` | `ASC` 或 `DESC` |

## 文档导航

| 文件 | 说明 |
|------|------|
| [`reference.md`](reference.md) | 完整 API 接口文档（参数、响应格式、错误处理） |
| [`examples.md`](examples.md) | 实用示例（搜索、分页、jq 过滤、批量操作） |
| [`scripts/outline.py`](scripts/outline.py) | Python CLI 脚本（可直接执行） |
