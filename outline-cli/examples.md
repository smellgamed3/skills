# Outline CLI 使用示例

> 按需加载 — 当需要具体调用示例时参阅本文档。

所有示例均使用 `uv run scripts/outline.py <接口名> '<JSON 参数>'` 格式。

---

## 集合操作

### 列出所有集合

```bash
# 列出所有活跃集合
uv run scripts/outline.py collections.list '{}'

# 只显示集合 id 和 name
uv run scripts/outline.py collections.list '{}' \
  | jq '[.data[] | {id, name}]'
```

### 按名称搜索集合

```bash
uv run scripts/outline.py collections.list '{"query": "工程"}'
```

### 获取集合的完整文档树

```bash
uv run scripts/outline.py collections.documents '{"id": "COLLECTION_UUID"}'

# 只显示一级文档标题
uv run scripts/outline.py collections.documents '{"id": "COLLECTION_UUID"}' \
  | jq '[.data[] | {title, url}]'
```

---

## 文档操作

### 按 ID 获取文档（含正文）

```bash
uv run scripts/outline.py documents.info '{"id": "DOC_UUID"}'

# 只输出正文（Markdown）
uv run scripts/outline.py documents.info '{"id": "DOC_UUID"}' \
  | jq -r '.data.text'
```

### 按共享链接获取文档

```bash
uv run scripts/outline.py documents.info '{"shareId": "SHARE_UUID"}'
```

### 列出集合内所有已发布文档

```bash
uv run scripts/outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "sort": "updatedAt",
  "direction": "DESC"
}'

# 只显示标题和更新时间
uv run scripts/outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"]
}' | jq '[.data[] | {title, updatedAt}]'
```

### 列出某用户创建的文档

```bash
uv run scripts/outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "userId": "USER_UUID",
  "statusFilter": ["published", "draft"]
}'
```

### 列出某文档的所有子文档

```bash
uv run scripts/outline.py documents.list '{
  "parentDocumentId": "PARENT_DOC_UUID"
}'
```

---

## 搜索操作

### 全文搜索

```bash
uv run scripts/outline.py documents.search '{"query": "部署流程"}'

# 限定在某集合内搜索（推荐，速度更快）
uv run scripts/outline.py documents.search '{
  "query": "部署流程",
  "collectionId": "COLLECTION_UUID"
}'

# 只搜索本月内更新的文档
uv run scripts/outline.py documents.search '{
  "query": "部署流程",
  "dateFilter": "month",
  "statusFilter": ["published"]
}'
```

### 提取搜索结果的标题和摘要

```bash
uv run scripts/outline.py documents.search '{"query": "API 接入"}' \
  | jq '[.data[] | {title: .document.title, context, ranking}]'
```

### 仅搜索文档标题（速度更快）

```bash
uv run scripts/outline.py documents.search_titles '{"query": "新员工入职"}'

# 限定集合
uv run scripts/outline.py documents.search_titles '{
  "query": "新员工入职",
  "collectionId": "COLLECTION_UUID"
}' | jq '[.data[] | {id, title}]'
```

---

## 分页处理

### 手动翻页

```bash
# 第 1 页
uv run scripts/outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "limit": 25,
  "offset": 0
}'

# 第 2 页
uv run scripts/outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "limit": 25,
  "offset": 25
}'
```

### Shell 脚本批量获取所有文档

```bash
#!/bin/bash
COLLECTION_UUID="your-collection-uuid"
OFFSET=0
LIMIT=25

while true; do
  RESULT=$(uv run scripts/outline.py documents.list "{
    \"collectionId\": \"$COLLECTION_UUID\",
    \"limit\": $LIMIT,
    \"offset\": $OFFSET
  }")

  # 输出本页标题
  echo "$RESULT" | jq -r '.data[].title'

  # 检查是否还有下一页
  COUNT=$(echo "$RESULT" | jq '.data | length')
  if [ "$COUNT" -lt "$LIMIT" ]; then
    break
  fi

  OFFSET=$((OFFSET + LIMIT))
done
```

---

## jq 过滤技巧

### 提取文档 ID 列表

```bash
uv run scripts/outline.py documents.list '{"collectionId": "COLL_UUID"}' \
  | jq -r '.data[].id'
```

### 按更新时间排序并只显示前 5 条

```bash
uv run scripts/outline.py documents.list '{
  "collectionId": "COLL_UUID",
  "sort": "updatedAt",
  "direction": "DESC",
  "limit": 5
}' | jq '[.data[] | {title, updatedAt}]'
```

### 搜索并只返回相关度高于阈值的结果

```bash
uv run scripts/outline.py documents.search '{"query": "API"}' \
  | jq '[.data[] | select(.ranking > 0.5) | {title: .document.title, ranking}]'
```

### 将结果保存到文件

```bash
uv run scripts/outline.py documents.search '{"query": "架构设计"}' \
  | jq '.' > search_results.json
```

---

## 常用工作流

### 查找并读取文档

```bash
# 第一步：按标题搜索，获取文档 ID
DOC_ID=$(uv run scripts/outline.py documents.search_titles \
  '{"query": "数据库设计规范"}' \
  | jq -r '.data[0].id')

echo "找到文档 ID：$DOC_ID"

# 第二步：读取完整内容
uv run scripts/outline.py documents.info "{\"id\": \"$DOC_ID\"}" \
  | jq -r '.data.text'
```

### 列出集合并选择目标集合

```bash
# 先列出所有集合
uv run scripts/outline.py collections.list '{}' \
  | jq -r '.data[] | "\(.id)  \(.name)"'

# 使用选定的集合 UUID 进行后续操作
COLL_UUID="选定的集合 UUID"
uv run scripts/outline.py documents.list "{\"collectionId\": \"$COLL_UUID\"}"
```
