# Outline API 接口参考

> 按需加载 — 当需要查询接口参数细节或排查错误时参阅本文档。

## API 基础

Outline 使用 RPC 风格 API：所有接口均通过向 `https://<host>/api/<method>` 发送 **POST** 请求调用，请求体和响应体均为 JSON。

```
POST https://<base_url>/api/<method>
Content-Type: application/json
Authorization: Bearer <api_key>
Accept: application/json
```

## 响应格式

### 成功响应

```json
{ "ok": true, "status": 200, "data": { ... } }
```

### 错误响应

```json
{ "ok": false, "error": "Not Found", "message": "..." }
```

### 分页列表响应

```json
{
  "ok": true,
  "data": [ ... ],
  "pagination": {
    "limit": 25,
    "offset": 0,
    "nextPath": "/api/documents.list?limit=25&offset=25"
  }
}
```

### 通用分页参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `limit` | integer | 25 | 每页返回条数，最大 100 |
| `offset` | integer | 0 | 起始偏移量 |
| `sort` | string | 各接口不同 | 排序字段名 |
| `direction` | string | `DESC` | `ASC` 或 `DESC` |

---

## 集合（Collections）

### `collections.info`

获取单个集合的详细信息。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string (UUID) | ✅ | 集合 UUID |

**示例：**
```bash
uv run scripts/outline.py collections.info '{"id": "COLLECTION_UUID"}'
```

**响应 `data` 字段：**
```json
{
  "id": "...",
  "name": "Engineering",
  "description": "...",
  "color": "#FF5733",
  "icon": "🚀",
  "permission": "read",
  "sharing": true,
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-06-01T00:00:00.000Z"
}
```

---

### `collections.list`

列出当前用户有权访问的所有集合。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ❌ | 按名称过滤 |
| `statusFilter` | string[] | ❌ | `["active"]`（目前仅 `active`） |
| `limit` | integer | ❌ | 默认 25 |
| `offset` | integer | ❌ | 默认 0 |

**示例：**
```bash
uv run scripts/outline.py collections.list '{
  "query": "engineering",
  "statusFilter": ["active"],
  "limit": 25,
  "offset": 0
}'
```

**响应 `data` 字段：** 集合对象数组（结构同 `collections.info`）。

---

### `collections.documents`

获取集合的完整文档树（嵌套导航节点）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string (UUID) | ✅ | 集合 UUID |

**示例：**
```bash
uv run scripts/outline.py collections.documents '{"id": "COLLECTION_UUID"}'
```

**响应 `data` 字段：** 导航节点的嵌套树，每个节点包含：
```json
{
  "id": "...",
  "title": "文档标题",
  "url": "/doc/...",
  "children": [ ... ]
}
```

---

## 文档（Documents）

### `documents.info`

获取单篇文档的完整信息，包括正文内容（Markdown）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ❌ | 文档 UUID 或 URL 中的 ID |
| `shareId` | string (UUID) | ❌ | 共享链接 UUID（公开文档） |

`id` 与 `shareId` 二选一，至少提供一个。

**示例：**
```bash
# 按文档 ID
uv run scripts/outline.py documents.info '{"id": "DOC_UUID"}'

# 按共享链接 ID
uv run scripts/outline.py documents.info '{"shareId": "SHARE_UUID"}'
```

**响应 `data` 字段：**
```json
{
  "id": "...",
  "title": "文档标题",
  "text": "# 正文（Markdown）\n...",
  "collectionId": "...",
  "parentDocumentId": null,
  "createdBy": { "id": "...", "name": "张三" },
  "updatedBy": { "id": "...", "name": "李四" },
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-06-01T00:00:00.000Z",
  "publishedAt": "2024-01-02T00:00:00.000Z",
  "archivedAt": null,
  "url": "/doc/...",
  "urlId": "..."
}
```

---

### `documents.list`

列出已发布文档，支持多种过滤条件。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string (UUID) | ❌ | 按集合过滤 |
| `userId` | string (UUID) | ❌ | 按创建者过滤 |
| `parentDocumentId` | string (UUID) | ❌ | 按父文档过滤（列出子文档） |
| `statusFilter` | string[] | ❌ | `["published"]`、`["draft"]`、`["archived"]` 或组合 |
| `limit` | integer | ❌ | 默认 25 |
| `offset` | integer | ❌ | 默认 0 |
| `sort` | string | ❌ | `updatedAt`、`createdAt`、`title` 等 |
| `direction` | string | ❌ | `ASC` 或 `DESC`（默认 `DESC`） |

**有效的 `statusFilter` 值：**
- `"published"` — 已发布文档
- `"draft"` — 草稿
- `"archived"` — 已归档文档

**示例：**
```bash
uv run scripts/outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "sort": "updatedAt",
  "direction": "DESC",
  "limit": 25,
  "offset": 0
}'
```

**响应 `data` 字段：** 文档对象数组（结构同 `documents.info`，不含 `text` 字段）。

---

### `documents.search`

在文档内容中进行全文搜索。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `collectionId` | string (UUID) | ❌ | 限定在特定集合内搜索（推荐） |
| `userId` | string (UUID) | ❌ | 限定创建者 |
| `statusFilter` | string[] | ❌ | 同 `documents.list` |
| `dateFilter` | string | ❌ | `day`、`week`、`month`、`year` |
| `snippetMinWords` | integer | ❌ | 摘要最少字数（默认 20） |
| `snippetMaxWords` | integer | ❌ | 摘要最多字数（默认 30） |
| `sort` | string | ❌ | `relevance`（默认）或 `updatedAt` |
| `direction` | string | ❌ | `ASC` 或 `DESC` |
| `limit` | integer | ❌ | 默认 25 |
| `offset` | integer | ❌ | 默认 0 |

**示例：**
```bash
uv run scripts/outline.py documents.search '{
  "query": "部署流程",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "dateFilter": "month",
  "limit": 25
}'
```

**响应 `data` 字段：** 搜索结果数组，每项包含：
```json
{
  "ranking": 0.95,
  "context": "...匹配的<b>文本片段</b>...",
  "document": { "id": "...", "title": "...", ... }
}
```

---

### `documents.search_titles`

仅在文档标题中搜索，速度比全文搜索快。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `collectionId` | string (UUID) | ❌ | 限定集合 |
| `statusFilter` | string[] | ❌ | 同 `documents.list` |
| `limit` | integer | ❌ | 默认 25 |
| `offset` | integer | ❌ | 默认 0 |

**示例：**
```bash
uv run scripts/outline.py documents.search_titles '{
  "query": "API 指南",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "limit": 25
}'
```

**响应 `data` 字段：** 文档对象数组（结构同 `documents.list`）。

---

## 错误处理

### 常见错误码

| HTTP 状态码 | 错误信息 | 原因 |
|------------|---------|------|
| 400 | `validation_error` | 请求参数格式错误 |
| 401 | `authentication_required` | API Key 无效或已过期 |
| 403 | `authorization_error` | 无权访问该资源 |
| 404 | `not_found` | 资源不存在（UUID 错误或已删除） |
| 429 | `rate_limit_exceeded` | 请求频率超限，稍后重试 |
| 500 | `server_error` | Outline 服务端错误 |

### 排查思路

**401 Unauthorized**
```bash
# 验证 API Key 是否有效
uv run scripts/outline.py auth.info '{}'
```
前往 Outline → 设置 → API 令牌，重新生成 Key。

**404 Not Found**
- 确认 UUID 正确（直接从文档 URL 复制）
- 确认文档/集合未被归档或删除

**`data` 数组为空**
- 尝试更宽泛的搜索词
- 去掉 `statusFilter` 以包含草稿和归档文档
- 确认 `collectionId` 正确

**配置文件读取失败**
```bash
# 检查配置文件是否存在且格式正确
cat ~/.config/outline.json | python3 -m json.tool
```

---

## 资源

- **Outline API 文档**：https://www.getoutline.com/developers（或私有部署实例的 `https://wiki.example.com/developers`）
- **uv 文档**：https://docs.astral.sh/uv/
- **jq 手册**：https://jqlang.github.io/jq/manual/
