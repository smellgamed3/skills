---
name: outline-cli
description: 当用户需要通过 API 与 Outline（wiki 知识库应用）交互时使用，包括：读取、搜索、列出文档集合和文档。兼容云端（app.getoutline.com）和私有部署实例。
---

# Outline API 技能文档

## 概述

Outline 是一款现代 wiki 知识库应用，提供完善的 RPC 风格 API。每个接口都是向 `https://<your-host>/api/:method` 发送 `POST` 请求，请求体和响应体均为 JSON 格式。

**配置文件：** `~/.config/outline.json`
```json
{
  "base_url": "https://app.getoutline.com",
  "api_key": "ol_api_..."
}
```

**运行方式（uv run）：**

将以下内容保存为 `outline.py`（首次运行时 uv 会自动安装依赖）：

```python
# /// script
# dependencies = ["requests"]
# ///
import json, sys, pathlib, requests

config = json.loads(pathlib.Path("~/.config/outline.json").expanduser().read_text())
base = config["base_url"].rstrip("/")
key  = config["api_key"]

method = sys.argv[1]
data   = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

resp = requests.post(
    f"{base}/api/{method}",
    json=data,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
)
print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
```

调用方式：
```bash
uv run outline.py <method> '<json>'
```

---

## 响应格式

**成功：**
```json
{ "ok": true, "status": 200, "data": { ... } }
```

**错误：**
```json
{ "ok": false, "error": "Not Found" }
```

**分页列表：**
```json
{
  "ok": true, "data": [...],
  "pagination": { "limit": 25, "offset": 0, "nextPath": "/api/documents.list?limit=25&offset=25" }
}
```

所有列表接口均支持分页参数：`limit`（默认 25）、`offset`。  
排序参数：`sort`（字段名）、`direction`（`ASC` | `DESC`）。

---

## 文档集合（Collections）

### `collections.info` — 获取知识库详情
```bash
uv run outline.py collections.info '{"id": "COLLECTION_UUID"}'
```

### `collections.list` — 列出所有知识库
```bash
uv run outline.py collections.list '{
  "query": "engineering",
  "statusFilter": ["active"],
  "limit": 25, "offset": 0
}'
```

### `collections.documents` — 获取知识库的完整文档树
```bash
uv run outline.py collections.documents '{"id": "COLLECTION_UUID"}'
```
返回导航节点的嵌套树结构。

---

## 文档（Documents）

### `documents.info` — 获取文档详情
```bash
uv run outline.py documents.info '{"id": "DOC_ID_OR_URL_ID"}'
# 通过 shareId 查询：
uv run outline.py documents.info '{"shareId": "SHARE_UUID"}'
```

### `documents.list` — 列出已发布文档
```bash
uv run outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "userId":       "USER_UUID",
  "parentDocumentId": "DOC_UUID",
  "statusFilter": ["published", "draft", "archived"],
  "limit": 25, "offset": 0,
  "sort": "updatedAt", "direction": "DESC"
}'
```

### `documents.search` — 全文搜索文档
```bash
uv run outline.py documents.search '{
  "query": "onboarding process",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "dateFilter": "month",
  "snippetMinWords": 20,
  "snippetMaxWords": 30,
  "sort": "relevance",
  "direction": "DESC",
  "limit": 25
}'
```
返回数组，每项包含 `{ context, ranking, document }`。

### `documents.search_titles` — 仅搜索文档标题（速度更快）
```bash
uv run outline.py documents.search_titles '{
  "query": "API guide",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "limit": 25
}'
```

---

## 接口速查表

| 资源 | 接口 | 关键参数 |
|------|------|----------|
| **文档集合** | `collections.info` | `id` |
| | `collections.list` | `query`、`statusFilter`、分页 |
| | `collections.documents` | `id` |
| **文档** | `documents.info` | `id` 或 `shareId` |
| | `documents.list` | `collectionId`、`userId`、`statusFilter`、分页 |
| | `documents.search` | `query`、过滤条件、分页 |
| | `documents.search_titles` | `query`、过滤条件、分页 |
