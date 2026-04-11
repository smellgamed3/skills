---
name: outline-cli
description: Use when interacting with Outline (wiki knowledge base) via its API, including reading, searching, and listing collections and documents. Works with both cloud (app.getoutline.com) and self-hosted instances.
---

# Outline CLI

## Overview

Outline is a modern wiki knowledge base with a complete RPC-style API. Every endpoint is a `POST` request to `https://<host>/api/<method>` with JSON body and response. This skill provides a lightweight Python CLI wrapper using `uv` to call the API directly from the terminal.

**Core principle:** One script, zero installation overhead — `uv run` handles dependencies automatically on first use.

## When to Use

```
Need to interact with Outline knowledge base?
│
├─ Read or inspect content?
│  ├─ Single document by ID/URL → documents.info
│  └─ Browse collection structure → collections.documents
│
├─ Search for content?
│  ├─ Full-text search → documents.search
│  └─ Title-only search (faster) → documents.search_titles
│
├─ List resources?
│  ├─ All collections → collections.list
│  └─ Documents in a collection → documents.list
│
└─ Get specific resource details?
   ├─ Collection metadata → collections.info
   └─ Document by shareId → documents.info (shareId)
```

**Use this skill when:**
- Looking up documents or collections in an Outline wiki
- Searching knowledge base content from the command line
- Automating Outline API calls in scripts or workflows
- Exploring the document tree of a collection

**When NOT to use:**
- For creating or modifying documents (use the Outline web app or write-capable API tokens)
- When no API key is available

## Setup

### Configuration File

Create `~/.config/outline.json`:
```json
{
  "base_url": "https://app.getoutline.com",
  "api_key": "ol_api_..."
}
```

For self-hosted instances, replace `base_url` with your instance URL (e.g., `https://wiki.example.com`).

### CLI Script

Save the following as `outline.py` (first run installs dependencies automatically via `uv`):

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

**Usage:**
```bash
uv run outline.py <method> '<json_payload>'
```

## Quick Reference

### API Methods

| Resource | Method | Key Parameters |
|----------|--------|----------------|
| **Collections** | `collections.info` | `id` |
| | `collections.list` | `query`, `statusFilter`, pagination |
| | `collections.documents` | `id` |
| **Documents** | `documents.info` | `id` or `shareId` |
| | `documents.list` | `collectionId`, `userId`, `statusFilter`, pagination |
| | `documents.search` | `query`, filters, pagination |
| | `documents.search_titles` | `query`, filters, pagination |

### Pagination Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `limit` | 25 | Results per page |
| `offset` | 0 | Starting position |
| `sort` | varies | Field to sort by |
| `direction` | `DESC` | `ASC` or `DESC` |

## Response Format

**Success:**
```json
{ "ok": true, "status": 200, "data": { ... } }
```

**Error:**
```json
{ "ok": false, "error": "Not Found" }
```

**Paginated list:**
```json
{
  "ok": true,
  "data": [...],
  "pagination": { "limit": 25, "offset": 0, "nextPath": "/api/documents.list?limit=25&offset=25" }
}
```

## Collections

### `collections.info` — Get collection details
```bash
uv run outline.py collections.info '{"id": "COLLECTION_UUID"}'
```

### `collections.list` — List all collections
```bash
uv run outline.py collections.list '{
  "query": "engineering",
  "statusFilter": ["active"],
  "limit": 25,
  "offset": 0
}'
```

### `collections.documents` — Get full document tree
```bash
uv run outline.py collections.documents '{"id": "COLLECTION_UUID"}'
```
Returns a nested tree of navigation nodes for the entire collection.

## Documents

### `documents.info` — Get document details
```bash
# By document ID
uv run outline.py documents.info '{"id": "DOC_ID_OR_URL_ID"}'

# By share ID
uv run outline.py documents.info '{"shareId": "SHARE_UUID"}'
```

### `documents.list` — List published documents
```bash
uv run outline.py documents.list '{
  "collectionId": "COLLECTION_UUID",
  "userId": "USER_UUID",
  "parentDocumentId": "DOC_UUID",
  "statusFilter": ["published", "draft", "archived"],
  "limit": 25,
  "offset": 0,
  "sort": "updatedAt",
  "direction": "DESC"
}'
```

### `documents.search` — Full-text search
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
Returns an array where each item contains `{ context, ranking, document }`.

### `documents.search_titles` — Search document titles only (faster)
```bash
uv run outline.py documents.search_titles '{
  "query": "API guide",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "limit": 25
}'
```

## Best Practices

### Narrow searches with collectionId

Always pass `collectionId` when you know the target collection — it dramatically reduces result noise and latency:
```bash
uv run outline.py documents.search '{"query": "deploy", "collectionId": "COLL_UUID"}'
```

### Use search_titles for discovery, search for content

- `documents.search_titles` is faster and ideal when you know the document name
- `documents.search` is better when you need to find content within documents

### Handle pagination for large workspaces

Check `pagination.nextPath` in the response and increment `offset` to fetch additional pages:
```bash
# Page 1
uv run outline.py documents.list '{"collectionId": "COLL_UUID", "limit": 25, "offset": 0}'

# Page 2
uv run outline.py documents.list '{"collectionId": "COLL_UUID", "limit": 25, "offset": 25}'
```

### Pretty-print and filter with jq

Pipe output through `jq` to extract specific fields:
```bash
# Get document titles from search results
uv run outline.py documents.search '{"query": "onboarding"}' | jq '[.data[].document | {id, title}]'

# List collection names
uv run outline.py collections.list '{}' | jq '[.data[] | {id, name}]'
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using GET instead of POST | All Outline API calls use POST — the CLI handles this automatically |
| Missing `Content-Type` header | The CLI sets all required headers automatically |
| Passing string instead of JSON object | Always wrap payload in single quotes: `'{"key": "val"}'` |
| Not paginating large results | Check `pagination.nextPath` and use `offset` to fetch all pages |
| Using wrong `statusFilter` values | Valid values: `"published"`, `"draft"`, `"archived"` |
| Searching without `collectionId` | Scope searches to a collection to reduce noise and improve speed |

## Troubleshooting

### `401 Unauthorized`
```bash
# Verify your API key is valid
uv run outline.py auth.info '{}'
```
Re-generate the API key in Outline → Settings → API Tokens.

### `404 Not Found`
- Confirm the UUID is correct (copy directly from the document URL)
- Ensure the document/collection hasn't been archived or deleted

### Empty `data` array
- The query matched nothing — try broader search terms
- Remove `statusFilter` to include drafts and archived documents
- Confirm the `collectionId` is correct

### `uv` not found
Install `uv` with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Config file not found
```bash
mkdir -p ~/.config
cat > ~/.config/outline.json << 'EOF'
{
  "base_url": "https://app.getoutline.com",
  "api_key": "ol_api_YOUR_KEY_HERE"
}
EOF
```

## Resources

- **Outline API Reference**: https://www.getoutline.com/developers
- **uv Documentation**: https://docs.astral.sh/uv/
- **jq Manual**: https://jqlang.github.io/jq/manual/

**Remember:** The Outline API is read/write — this skill focuses on read operations. Always scope searches with a `collectionId` when possible for better performance.
