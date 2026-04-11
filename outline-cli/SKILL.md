---
name: outline-cli
description: 当用户需要通过 API 与 Outline（wiki 知识库应用）交互时使用，包括：创建、读取、更新、删除、搜索、归档、移动或复制文档；管理知识库、评论、用户、用户组、分享链接、星标、模板、历史版本、附件、文件操作、事件或数据属性；以及检查认证信息。支持 API Key 和 OAuth，兼容云端（app.getoutline.com）和私有部署实例。
---

# Outline API 技能文档

## 概述

Outline 是一款现代 wiki 知识库应用，提供完善的 RPC 风格 API。每个接口都是向 `https://app.getoutline.com/api/:method`（或你的私有部署域名）发送 `POST` 请求，请求体和响应体均为 JSON 格式。

**使用前设置环境变量：**
```bash
export OUTLINE_API_KEY="ol_api_..."          # required
export OUTLINE_API_BASE="https://app.getoutline.com"  # or your self-hosted URL
```

**可复用的辅助函数（bash）：**
```bash
outline() {
  local method="$1" data="${2:-{}}"
  curl -sf "${OUTLINE_API_BASE:-https://app.getoutline.com}/api/${method}" \
    -X POST \
    -H "Authorization: Bearer ${OUTLINE_API_KEY:?OUTLINE_API_KEY not set}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$data"
}
```

---

## 决策树

```
你需要做什么？
│
├─ 操作文档？                    → documents.*
├─ 管理知识库？                   → collections.*
├─ 添加/读取评论？                → comments.*
├─ 管理用户？                     → users.*
├─ 管理用户组？                   → groups.*
├─ 公开分享文档？                 → shares.*
├─ 收藏/星标内容？                → stars.*
├─ 查看文档历史版本？              → revisions.*
├─ 使用模板？                     → templates.*
├─ 上传/管理文件附件？            → attachments.*
├─ 批量导入/导出数据？            → collections.export* / fileOperations.*
├─ 审计日志/操作流水？            → events.list
├─ 自定义元数据字段？             → dataAttributes.*（商业版/企业版）
└─ 检查 API 认证/工作区信息？     → auth.*
```

---

## 认证

| 方式 | 说明 |
|------|------|
| **API Key** | `Authorization: Bearer ol_api_<38位字符>`，在 **设置 → API & 应用** 中创建。 |
| **OAuth 2.0** | 在 **设置 → 应用** 中注册应用，然后用客户端凭据换取访问令牌。 |

**权限范围**（限制 API Key 访问权限）：

| 范围 | 授权内容 |
|------|----------|
| `read` | 所有读取操作 |
| `write` | 所有读取 + 写入操作 |
| `documents:read` | 仅文档读取 |
| `documents:write` | 文档读写 |
| `collections:read` | 仅知识库读取 |
| `collections:write` | 知识库读写 |
| `documents.*` | 所有文档 API 方法 |
| `users.*` | 所有用户 API 方法 |

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

## Auth（认证）

### `auth.info` — 获取当前认证信息
```bash
outline auth.info
```
返回当前 API Key 关联的用户和团队信息。

### `auth.config` — 获取认证配置（公开接口，无需认证）
```bash
outline auth.config
```
返回工作区可用的认证提供商（SSO 服务）列表。

---

## 文档（Documents）

### `documents.info` — 获取文档详情
```bash
outline documents.info '{"id": "DOC_ID_OR_URL_ID"}'
# Or by share ID:
outline documents.info '{"shareId": "SHARE_UUID"}'
```

### `documents.list` — 列出所有已发布文档
```bash
outline documents.list '{
  "collectionId": "COLLECTION_UUID",   // optional: filter by collection
  "userId":       "USER_UUID",         // optional: filter by creator
  "parentDocumentId": "DOC_UUID",      // optional: filter children of a doc
  "backlinkDocumentId": "DOC_UUID",    // optional: docs that link to this doc
  "statusFilter": ["published","draft","archived"],
  "limit": 25, "offset": 0,
  "sort": "updatedAt", "direction": "DESC"
}'
```

### `documents.drafts` — 列出当前用户的草稿文档
```bash
outline documents.drafts '{
  "collectionId": "COLLECTION_UUID",   // optional
  "dateFilter": "week",                // optional: day | week | month | year
  "limit": 25, "offset": 0
}'
```

### `documents.archived` — 列出已归档文档
```bash
outline documents.archived '{"collectionId": "COLLECTION_UUID", "limit": 25}'
```

### `documents.deleted` — 列出已删除（回收站）文档
```bash
outline documents.deleted '{"limit": 25, "offset": 0}'
```

### `documents.viewed` — 列出最近浏览的文档
```bash
outline documents.viewed '{"limit": 25}'
```

### `documents.documents` — 获取文档的子文档结构（树形）
```bash
outline documents.documents '{"id": "DOC_ID"}'
```

### `documents.search` — 全文搜索文档
```bash
outline documents.search '{
  "query": "onboarding process",
  "collectionId": "COLLECTION_UUID",   // optional
  "userId":       "USER_UUID",         // optional
  "documentId":   "DOC_UUID",          // optional: search within subtree
  "statusFilter": ["published"],
  "dateFilter":   "month",             // optional: day|week|month|year
  "shareId":      "SHARE_UUID",        // optional
  "snippetMinWords": 20,
  "snippetMaxWords": 30,
  "sort": "relevance",                 // relevance|createdAt|updatedAt|title
  "direction": "DESC",
  "limit": 25
}'
```
返回数组，每项包含 `{ context, ranking, document }`。

### `documents.search_titles` — 仅搜索文档标题（速度更快）
```bash
outline documents.search_titles '{
  "query": "API guide",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "limit": 25
}'
```

### `documents.answerQuestion` — 用自然语言提问文档内容 *(商业版/企业版/云端)*
```bash
outline documents.answerQuestion '{
  "query": "What is our holiday policy?",
  "collectionId": "COLLECTION_UUID"
}'
```

### `documents.create` — 创建文档
```bash
outline documents.create '{
  "title": "Document Title",
  "text": "# Heading\n\nContent in **markdown**.",
  "collectionId": "COLLECTION_UUID",      // required unless parentDocumentId set
  "parentDocumentId": "PARENT_DOC_UUID",  // optional: nest under a parent
  "templateId": "TEMPLATE_UUID",          // optional: base on a template
  "publish": true,                        // false = save as draft
  "fullWidth": false,
  "icon": "📄",
  "color": "#FF5733",
  "createdAt": "2024-01-01T00:00:00Z"    // optional: backdate creation
}'
```

### `documents.update` — 更新文档
```bash
outline documents.update '{
  "id": "DOC_ID",
  "title": "Updated Title",
  "text": "Updated content in markdown.",
  "publish": true,          // draft → published
  "fullWidth": false,
  "icon": "📝",
  "color": "#123456",
  "collectionId": "UUID",   // move to different collection
  "insightsEnabled": true,
  "editMode": "replace"     // replace | append | prepend
}'
```

### `documents.duplicate` — 复制文档
```bash
outline documents.duplicate '{
  "id": "DOC_ID",
  "title": "Copy of Original",
  "recursive": true,              // duplicate child docs too
  "publish": false,
  "collectionId": "COLLECTION_UUID",
  "parentDocumentId": "PARENT_UUID"
}'
```

### `documents.move` — 移动文档
```bash
outline documents.move '{
  "id": "DOC_ID",
  "collectionId": "TARGET_COLLECTION_UUID",
  "parentDocumentId": "NEW_PARENT_UUID",  // omit = collection root
  "index": 0                              // optional: position in list
}'
```

### `documents.archive` — 归档文档
```bash
outline documents.archive '{"id": "DOC_ID"}'
```

### `documents.restore` — 恢复已归档或已删除的文档
```bash
outline documents.restore '{
  "id": "DOC_ID",
  "collectionId": "COLLECTION_UUID",  // optional: restore to specific collection
  "revisionId":   "REVISION_UUID"     // optional: restore to a past revision
}'
```

### `documents.unpublish` — 将已发布文档退回草稿
```bash
outline documents.unpublish '{"id": "DOC_ID", "detach": false}'
```

### `documents.delete` — 删除文档（移入回收站）
```bash
outline documents.delete '{"id": "DOC_ID"}'
# 永久销毁（不可恢复）：
outline documents.delete '{"id": "DOC_ID", "permanent": true}'
```

### `documents.export` — 将文档导出为 Markdown/HTML/PDF
```bash
# Markdown（默认 Accept 头）：
outline documents.export '{"id": "DOC_ID"}'
# 包含子文档（返回 zip）：
outline documents.export '{"id": "DOC_ID", "includeChildDocuments": true}'
# 指定纸张大小导出 PDF：
outline documents.export '{"id": "DOC_ID", "paperSize": "A4"}'
```

### `documents.import` — 从文件导入为文档
```bash
curl -sf "${OUTLINE_API_BASE}/api/documents.import" \
  -X POST \
  -H "Authorization: Bearer ${OUTLINE_API_KEY}" \
  -F "file=@/path/to/file.md" \
  -F "collectionId=COLLECTION_UUID" \
  -F "publish=true"
```
支持的文件类型：纯文本、Markdown、DOCX、CSV、TSV、HTML。

### `documents.templatize` — 将文档转换为模板
```bash
outline documents.templatize '{
  "id": "DOC_ID",
  "collectionId": "COLLECTION_UUID",
  "publish": true
}'
```

### `documents.users` — 列出所有有权访问该文档的用户
```bash
outline documents.users '{"id": "DOC_ID", "query": "alice"}'
```

### `documents.memberships` — 列出直接成员权限的用户
```bash
outline documents.memberships '{"id": "DOC_ID", "permission": "read"}'
```

### `documents.add_user` — 授予用户对文档的访问权限
```bash
outline documents.add_user '{"id": "DOC_ID", "userId": "USER_UUID", "permission": "read"}'
```

### `documents.remove_user` — 撤销用户对文档的访问权限
```bash
outline documents.remove_user '{"id": "DOC_ID", "userId": "USER_UUID"}'
```

### `documents.add_group` — 授予用户组对文档的访问权限
```bash
outline documents.add_group '{"id": "DOC_ID", "groupId": "GROUP_UUID", "permission": "read"}'
```

### `documents.remove_group` — 撤销用户组对文档的访问权限
```bash
outline documents.remove_group '{"id": "DOC_ID", "groupId": "GROUP_UUID"}'
```

---

## 知识库（Collections）

### `collections.info` — 获取知识库详情
```bash
outline collections.info '{"id": "COLLECTION_UUID"}'
```

### `collections.list` — 列出所有知识库
```bash
outline collections.list '{
  "query": "engineering",
  "statusFilter": ["active"],
  "limit": 25, "offset": 0
}'
```

### `collections.documents` — 获取知识库的完整文档树
```bash
outline collections.documents '{"id": "COLLECTION_UUID"}'
```
返回导航节点的嵌套树结构。

### `collections.create` — 创建知识库
```bash
outline collections.create '{
  "name": "Engineering",
  "description": "Technical documentation.",
  "permission": "read",     // read | read_write | null (private)
  "icon": "🛠️",
  "color": "#4A90E2",
  "sharing": true
}'
```

### `collections.update` — 更新知识库
```bash
outline collections.update '{
  "id": "COLLECTION_UUID",
  "name": "Engineering (Updated)",
  "description": "Updated description.",
  "permission": "read_write",
  "sharing": false
}'
```

### `collections.delete` — 删除知识库及其所有文档
```bash
outline collections.delete '{"id": "COLLECTION_UUID"}'
```
⚠️ 不可逆操作——将删除知识库内所有文档。

### `collections.export` — 将知识库导出为 zip 包
```bash
outline collections.export '{
  "id": "COLLECTION_UUID",
  "format": "outline-markdown"   // outline-markdown | json | html
}'
```
返回一个 `FileOperation`，通过 `fileOperations.info` 轮询状态和下载链接。

### `collections.export_all` — 导出所有知识库
```bash
outline collections.export_all '{
  "format": "outline-markdown",
  "includeAttachments": true,
  "includePrivate": true
}'
```

### `collections.memberships` — 列出知识库的用户成员权限
```bash
outline collections.memberships '{
  "id": "COLLECTION_UUID",
  "query": "jenny",
  "permission": "read",
  "limit": 25
}'
```

### `collections.add_user` — 将用户添加到知识库
```bash
outline collections.add_user '{
  "id": "COLLECTION_UUID",
  "userId": "USER_UUID",
  "permission": "read_write"
}'
```

### `collections.remove_user` — 将用户从知识库移除
```bash
outline collections.remove_user '{"id": "COLLECTION_UUID", "userId": "USER_UUID"}'
```

### `collections.group_memberships` — 列出知识库的用户组权限
```bash
outline collections.group_memberships '{"id": "COLLECTION_UUID", "query": "devs"}'
```

### `collections.add_group` — 授予用户组对知识库的访问权限
```bash
outline collections.add_group '{
  "id": "COLLECTION_UUID",
  "groupId": "GROUP_UUID",
  "permission": "read"
}'
```

### `collections.remove_group` — 撤销用户组对知识库的访问权限
```bash
outline collections.remove_group '{"id": "COLLECTION_UUID", "groupId": "GROUP_UUID"}'
```

---

## 评论（Comments）

### `comments.list` — 列出评论
```bash
outline comments.list '{
  "documentId": "DOC_UUID",         // optional: filter by document
  "collectionId": "COLLECTION_UUID",// optional: filter by collection
  "includeAnchorText": true,
  "limit": 25, "offset": 0
}'
```

### `comments.info` — 获取单条评论详情
```bash
outline comments.info '{"id": "COMMENT_UUID", "includeAnchorText": true}'
```

### `comments.create` — 发表评论或回复
```bash
outline comments.create '{
  "documentId": "DOC_UUID",
  "text": "This section needs clarification.",
  "parentCommentId": "PARENT_UUID"   // optional: make it a reply
}'
```

### `comments.update` — 更新评论
```bash
outline comments.update '{"id": "COMMENT_UUID", "data": {"text": "Updated text."}}'
```

### `comments.delete` — 删除评论（及其所有回复）
```bash
outline comments.delete '{"id": "COMMENT_UUID"}'
```

---

## 用户（Users）

### `users.info` — 获取用户信息
```bash
outline users.info '{"id": "USER_UUID"}'
```

### `users.list` — 列出工作区中的所有用户
```bash
outline users.list '{
  "query": "alice",
  "filter": "active",    // active | suspended | invited | all
  "role": "member",      // admin | member | viewer | guest
  "limit": 25, "offset": 0
}'
```

### `users.update` — 更新用户资料
```bash
outline users.update '{"id": "USER_UUID", "name": "Alice Smith", "avatarUrl": "https://..."}'
```

### `users.promote` — 将用户提升为管理员
```bash
outline users.promote '{"id": "USER_UUID"}'
```

### `users.demote` — 将管理员降级为成员/查看者
```bash
outline users.demote '{"id": "USER_UUID", "to": "member"}'
```

### `users.suspend` — 停用用户（撤销访问权限）
```bash
outline users.suspend '{"id": "USER_UUID"}'
```

### `users.activate` — 重新激活已停用的用户
```bash
outline users.activate '{"id": "USER_UUID"}'
```

### `users.delete` — 从工作区删除用户
```bash
outline users.delete '{"id": "USER_UUID"}'
```

---

## 用户组（Groups）

### `groups.info` — 获取用户组详情
```bash
outline groups.info '{"id": "GROUP_UUID"}'
```

### `groups.list` — 列出所有用户组
```bash
outline groups.list '{"query": "engineering", "limit": 25}'
```

### `groups.create` — 创建用户组
```bash
outline groups.create '{"name": "Backend Team"}'
```

### `groups.update` — 更新用户组
```bash
outline groups.update '{"id": "GROUP_UUID", "name": "Backend Engineers"}'
```

### `groups.delete` — 删除用户组
```bash
outline groups.delete '{"id": "GROUP_UUID"}'
```

### `groups.memberships` — 列出用户组中的成员
```bash
outline groups.memberships '{"id": "GROUP_UUID", "query": "bob", "limit": 25}'
```

### `groups.add_user` — 将用户添加到用户组
```bash
outline groups.add_user '{"id": "GROUP_UUID", "userId": "USER_UUID"}'
```

### `groups.remove_user` — 将用户从用户组移除
```bash
outline groups.remove_user '{"id": "GROUP_UUID", "userId": "USER_UUID"}'
```

---

## 分享（Shares）

### `shares.info` — 获取分享链接详情
```bash
outline shares.info '{"id": "SHARE_UUID"}'
# Or by document:
outline shares.info '{"documentId": "DOC_UUID"}'
```

### `shares.list` — 列出所有分享链接
```bash
outline shares.list '{"limit": 25, "offset": 0}'
```

### `shares.create` — 创建公开分享链接
```bash
outline shares.create '{
  "documentId": "DOC_UUID",
  "published": true,
  "includeChildDocuments": false,
  "urlId": "custom-slug"
}'
```

### `shares.update` — 更新分享设置
```bash
outline shares.update '{
  "id": "SHARE_UUID",
  "published": false,
  "includeChildDocuments": true
}'
```

### `shares.revoke` — 撤销分享链接
```bash
outline shares.revoke '{"id": "SHARE_UUID"}'
```

---

## 星标（Stars / 收藏夹）

### `stars.list` — 列出已收藏的内容
```bash
outline stars.list '{"limit": 25}'
```

### `stars.create` — 收藏文档或知识库
```bash
outline stars.create '{"documentId": "DOC_UUID"}'
outline stars.create '{"collectionId": "COLLECTION_UUID"}'
```

### `stars.delete` — 取消收藏
```bash
outline stars.delete '{"id": "STAR_UUID"}'
```

---

## 历史版本（Revisions）

### `revisions.info` — 获取特定历史版本
```bash
outline revisions.info '{"id": "REVISION_UUID"}'
```

### `revisions.list` — 列出文档的所有历史版本
```bash
outline revisions.list '{"documentId": "DOC_UUID", "limit": 25, "offset": 0}'
```

---

## 模板（Templates）

### `templates.info` — 获取模板详情
```bash
outline templates.info '{"id": "TEMPLATE_UUID"}'
```

### `templates.list` — 列出模板
```bash
outline templates.list '{
  "collectionId": "COLLECTION_UUID",  // optional: collection-scoped templates
  "limit": 25
}'
```

### `templates.update` — 更新模板
```bash
outline templates.update '{"id": "TEMPLATE_UUID", "title": "New Title", "text": "# Updated"}'
```

### `templates.delete` — 删除模板
```bash
outline templates.delete '{"id": "TEMPLATE_UUID"}'
```

---

## 附件（Attachments）

### `attachments.create` — 注册附件并获取上传 URL
```bash
outline attachments.create '{
  "name": "diagram.png",
  "contentType": "image/png",
  "size": 204800,
  "documentId": "DOC_UUID"   // optional: associate with a document
}'
```
返回 `{ uploadUrl, form, attachment }`，使用签名的 `uploadUrl` 将文件直接 PUT 到云存储。

### `attachments.redirect` — 获取附件的签名下载 URL
```bash
outline attachments.redirect '{"id": "ATTACHMENT_UUID"}'
```
返回 `302` 重定向到（可能带签名的）文件 URL。

### `attachments.delete` — 删除附件
```bash
outline attachments.delete '{"id": "ATTACHMENT_UUID"}'
```

---

## 文件操作（File Operations / 批量导入导出任务）

文件操作是用于批量导入/导出的后台任务。

### `fileOperations.info` — 轮询文件操作状态
```bash
outline fileOperations.info '{"id": "FILE_OPERATION_UUID"}'
```
检查 `data.state`：`creating` → `uploading` → `complete` | `error`。

### `fileOperations.list` — 列出文件操作记录
```bash
outline fileOperations.list '{"type": "export", "limit": 25}'
```

### `fileOperations.redirect` — 下载输出文件
```bash
outline fileOperations.redirect '{"id": "FILE_OPERATION_UUID"}'
```
当状态为 `complete` 时，返回 `302` 重定向到下载 URL。

### `fileOperations.delete` — 删除文件操作记录
```bash
outline fileOperations.delete '{"id": "FILE_OPERATION_UUID"}'
```

---

## 事件（Events / 审计日志）

### `events.list` — 列出操作事件
```bash
outline events.list '{
  "name": "documents.update",   // optional: filter by event name
  "documentId": "DOC_UUID",     // optional
  "collectionId": "COLLECTION_UUID",
  "userId": "USER_UUID",
  "actorId": "USER_UUID",
  "auditLog": true,
  "limit": 25, "offset": 0
}'
```
适用于审计追踪、操作流水和监控变更。

---

## 数据属性（Data Attributes）*(仅商业版/企业版)*

可附加到文档的自定义元数据字段。

### `dataAttributes.list` — 列出所有数据属性
```bash
outline dataAttributes.list '{"limit": 25}'
```

### `dataAttributes.info` — 获取数据属性详情
```bash
outline dataAttributes.info '{"id": "DATA_ATTR_UUID"}'
```

### `dataAttributes.create` — 创建数据属性
```bash
outline dataAttributes.create '{
  "name": "Status",
  "description": "Current status of the document.",
  "dataType": "string",   // string | boolean | number | list
  "options": {"values": ["Draft", "Review", "Published"]},
  "pinned": true
}'
```

### `dataAttributes.update` — 更新数据属性
```bash
outline dataAttributes.update '{
  "id": "DATA_ATTR_UUID",
  "name": "Priority",
  "options": {"values": ["Low", "Medium", "High"]},
  "pinned": false
}'
```
注意：`dataType` 创建后不可更改。

### `dataAttributes.delete` — 删除数据属性
```bash
outline dataAttributes.delete '{"id": "DATA_ATTR_UUID"}'
```

---

## 完整接口速查表

| 资源 | 接口 | 关键参数 |
|------|------|----------|
| **Auth** | `auth.info` | — |
| | `auth.config` | —（无需认证） |
| **文档** | `documents.info` | `id` 或 `shareId` |
| | `documents.list` | `collectionId`、`userId`、`statusFilter`、分页 |
| | `documents.drafts` | `collectionId`、`dateFilter`、分页 |
| | `documents.archived` | `collectionId`、分页 |
| | `documents.deleted` | 分页 |
| | `documents.viewed` | 分页 |
| | `documents.documents` | `id` |
| | `documents.search` | `query`、过滤条件、分页 |
| | `documents.search_titles` | `query`、过滤条件、分页 |
| | `documents.answerQuestion` ✨ | `query`、`collectionId` |
| | `documents.create` | `title`、`text`、`collectionId`、`publish` |
| | `documents.update` | `id`、`title`、`text`、`publish` |
| | `documents.duplicate` | `id`、`recursive`、`collectionId` |
| | `documents.move` | `id`、`collectionId`、`parentDocumentId` |
| | `documents.archive` | `id` |
| | `documents.restore` | `id`、`collectionId`、`revisionId` |
| | `documents.unpublish` | `id`、`detach` |
| | `documents.delete` | `id`、`permanent` |
| | `documents.export` | `id`、`includeChildDocuments`、`paperSize` |
| | `documents.import` | `file`（multipart）、`collectionId`、`publish` |
| | `documents.templatize` | `id`、`collectionId`、`publish` |
| | `documents.users` | `id`、`query` |
| | `documents.memberships` | `id`、`permission` |
| | `documents.add_user` | `id`、`userId`、`permission` |
| | `documents.remove_user` | `id`、`userId` |
| | `documents.add_group` | `id`、`groupId`、`permission` |
| | `documents.remove_group` | `id`、`groupId` |
| **知识库** | `collections.info` | `id` |
| | `collections.list` | `query`、`statusFilter`、分页 |
| | `collections.documents` | `id` |
| | `collections.create` | `name`、`permission`、`icon`、`color` |
| | `collections.update` | `id`、`name`、`permission`、`sharing` |
| | `collections.delete` | `id` |
| | `collections.export` | `id`、`format` |
| | `collections.export_all` | `format`、`includeAttachments` |
| | `collections.memberships` | `id`、`query`、`permission`、分页 |
| | `collections.add_user` | `id`、`userId`、`permission` |
| | `collections.remove_user` | `id`、`userId` |
| | `collections.group_memberships` | `id`、`query`、分页 |
| | `collections.add_group` | `id`、`groupId`、`permission` |
| | `collections.remove_group` | `id`、`groupId` |
| **评论** | `comments.list` | `documentId`、`collectionId`、分页 |
| | `comments.info` | `id`、`includeAnchorText` |
| | `comments.create` | `documentId`、`text`、`parentCommentId` |
| | `comments.update` | `id`、`data` |
| | `comments.delete` | `id` |
| **用户** | `users.info` | `id` |
| | `users.list` | `query`、`filter`、`role`、分页 |
| | `users.update` | `id`、`name`、`avatarUrl` |
| | `users.promote` | `id` |
| | `users.demote` | `id`、`to` |
| | `users.suspend` | `id` |
| | `users.activate` | `id` |
| | `users.delete` | `id` |
| **用户组** | `groups.info` | `id` |
| | `groups.list` | `query`、分页 |
| | `groups.create` | `name` |
| | `groups.update` | `id`、`name` |
| | `groups.delete` | `id` |
| | `groups.memberships` | `id`、`query`、分页 |
| | `groups.add_user` | `id`、`userId` |
| | `groups.remove_user` | `id`、`userId` |
| **分享** | `shares.info` | `id` 或 `documentId` |
| | `shares.list` | 分页 |
| | `shares.create` | `documentId`、`published`、`urlId` |
| | `shares.update` | `id`、`published`、`includeChildDocuments` |
| | `shares.revoke` | `id` |
| **星标** | `stars.list` | 分页 |
| | `stars.create` | `documentId` 或 `collectionId` |
| | `stars.delete` | `id` |
| **历史版本** | `revisions.info` | `id` |
| | `revisions.list` | `documentId`、分页 |
| **模板** | `templates.info` | `id` |
| | `templates.list` | `collectionId`、分页 |
| | `templates.update` | `id`、`title`、`text` |
| | `templates.delete` | `id` |
| **附件** | `attachments.create` | `name`、`contentType`、`size`、`documentId` |
| | `attachments.redirect` | `id` |
| | `attachments.delete` | `id` |
| **文件操作** | `fileOperations.info` | `id` |
| | `fileOperations.list` | `type`、分页 |
| | `fileOperations.redirect` | `id` |
| | `fileOperations.delete` | `id` |
| **事件** | `events.list` | `name`、`documentId`、`userId`、`auditLog`、分页 |
| **数据属性** ✨ | `dataAttributes.info` | `id` |
| | `dataAttributes.list` | 分页 |
| | `dataAttributes.create` | `name`、`dataType`、`options`、`pinned` |
| | `dataAttributes.update` | `id`、`name`、`options` |
| | `dataAttributes.delete` | `id` |

✨ = 需要商业版/企业版/云端套餐。

---

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| `200` / `201` | 成功 | — |
| `400` | 参数校验失败 | 检查请求体必填字段 |
| `401` | 未认证 | 检查 API Key 是否有效且未被撤销 |
| `403` | 未授权 | 检查 API Key 是否具备所需权限范围 |
| `404` | 资源不存在 | 确认资源 ID 是否正确 |
| `429` | 请求频率超限 | 等待 `Retry-After` 秒后重试，采用指数退避策略 |

---

## 常见错误

| 错误 | 解决方法 |
|------|----------|
| 使用 GET 而非 POST | Outline API 所有接口均为 `POST` |
| 缺少 `Content-Type: application/json` 请求头 | 必须始终包含此请求头 |
| 在代码中硬编码 API Key | 使用 `OUTLINE_API_KEY` 环境变量 |
| 忽略分页 | 使用 `nextPath` 或递增 `offset`（步长为 `limit`） |
| 导出后未轮询 `fileOperations.info` | 导出是异步操作，需轮询直到 `state === "complete"` |
| 创建时忘记设置 `publish: true` | 不设置则文档保存为草稿 |
| 意外永久删除 | 默认删除进入回收站（可恢复），设置 `permanent: true` 才会彻底销毁 |

---

## 私有部署实例

在所有调用中替换基础 URL：
```bash
export OUTLINE_API_BASE="https://wiki.yourcompany.com"
# 之后直接使用相同的 outline() 辅助函数，无需其他改动
```

## 参考资源

- **官方 API 文档：** https://www.getoutline.com/developers
- **OpenAPI 规范：** https://github.com/outline/openapi
- **API Key 管理：** 设置 → API & 应用
- **OAuth 应用注册：** 设置 → 应用
