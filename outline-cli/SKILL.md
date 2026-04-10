---
name: outline-cli
description: Use when the user wants to create, read, update, or delete documents and collections in Outline (the wiki and knowledge base app), search for content, manage comments, or interact with Outline's API programmatically. Supports authentication via API keys and OAuth.
---

# Outline CLI

## Overview

Outline is a modern wiki and knowledge base application with a comprehensive RPC-style API. This skill provides guidance for interacting with Outline documents, collections, comments, and user management through API calls.

**Core principle:** Outline uses an RPC-style API where all endpoints are POST requests to `https://app.getoutline.com/api/:method` with JSON payloads.

## When to Use

```
User wants to work with Outline documents, collections, or search?
│
├─ Create/read/update/delete documents?
│  └─ Use documents.* endpoints
│
├─ Manage collections (create/list/update)?
│  └─ Use collections.* endpoints
│
├─ Search for content across documents?
│  └─ Use documents.search endpoint
│
├─ Work with comments or discussions?
│  └─ Use comments.* endpoints
│
└─ Manage users or authentication?
   └─ Use users.* or auth.* endpoints
```

**Use this skill when:**
- Creating, reading, updating, or deleting Outline documents
- Managing collections and organizing content
- Searching for documents or content
- Working with comments and discussions
- Managing users and permissions
- Integrating Outline with other tools via API

**When NOT to use:**
- For general note-taking (use Blinko or other note tools)
- For simple document storage without Outline's features
- When user doesn't have an Outline workspace or API credentials

## Quick Reference

### Authentication

| Method | Description |
|--------|-------------|
| API Key | Bearer token in `Authorization` header. Format: `ol_api_` + 38 chars |
| OAuth 2.0 | Register app in Settings → Applications, exchange for access token |

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `documents.list` | POST | List all documents with pagination |
| `documents.info` | POST | Get details of a specific document |
| `documents.create` | POST | Create a new document |
| `documents.update` | POST | Update an existing document |
| `documents.delete` | POST | Delete a document |
| `documents.search` | POST | Search across documents |
| `collections.list` | POST | List all collections |
| `collections.create` | POST | Create a new collection |
| `collections.update` | POST | Update a collection |
| `comments.create` | POST | Create a comment on a document |
| `users.list` | POST | List all users |

## API Structure

### Request Format

All requests follow this pattern:

```bash
curl https://app.getoutline.com/api/<method> \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -H 'accept: application/json' \
  -d '{"param1": "value1", "param2": "value2"}'
```

### Response Format

**Success response:**
```json
{
  "ok": true,
  "status": 200,
  "data": { ... }
}
```

**Error response:**
```json
{
  "ok": false,
  "error": "Error message"
}
```

### Pagination

List endpoints support pagination:
```json
{
  "ok": true,
  "data": [...],
  "pagination": {
    "limit": 25,
    "offset": 0,
    "nextPath": "/api/documents.list?limit=25&offset=25"
  }
}
```

## Common Operations

### Document Operations

**List documents:**
```bash
curl https://app.getoutline.com/api/documents.list \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{"limit": 50, "offset": 0}'
```

**Create a document:**
```bash
curl https://app.getoutline.com/api/documents.create \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{
    "title": "Document Title",
    "text": "# Content\n\nDocument content here...",
    "collectionId": "collection_id",
    "parentDocumentId": "optional_parent_id"
  }'
```

**Update a document:**
```bash
curl https://app.getoutline.com/api/documents.update \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{
    "id": "document_id",
    "title": "Updated Title",
    "text": "# Updated Content\n\nNew content..."
  }'
```

**Get document info:**
```bash
curl https://app.getoutline.com/api/documents.info \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{"id": "document_id"}'
```

**Delete a document:**
```bash
curl https://app.getoutline.com/api/documents.delete \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{"id": "document_id"}'
```

### Collection Operations

**List collections:**
```bash
curl https://app.getoutline.com/api/collections.list \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{}'
```

**Create a collection:**
```bash
curl https://app.getoutline.com/api/collections.create \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{
    "name": "Collection Name",
    "description": "Collection description"
  }'
```

### Search Operations

**Search documents:**
```bash
curl https://app.getoutline.com/api/documents.search \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{
    "query": "search term",
    "limit": 25
  }'
```

## Scopes and Permissions

API keys can be scoped to limit access:

| Scope | Description |
|-------|-------------|
| `read` | Allows all read actions |
| `write` | Allows all read and write actions |
| `documents:read` | Allows only document read operations |
| `documents:write` | Allows document write operations |
| `collections:read` | Allows collection read operations |
| `collections:write` | Allows collection write operations |
| `documents.*` | Allows all document API methods |
| `users.*` | Allows all user API methods |

## Error Handling

**Common status codes:**
- `200/201` - Success
- `401` - Unauthenticated (invalid or revoked API key)
- `429` - Rate limit exceeded (check `Retry-After` header)

**Rate limiting:**
- Mutating endpoints are more restrictive than read-only
- Check `Retry-After` header on 429 responses
- Implement exponential backoff for retries

## Implementation Notes

### API Key Security

**CRITICAL:** Treat API keys like passwords
- Never commit API keys to source control
- Use environment variables: `OUTLINE_API_KEY=ol_api_xxx`
- Rotate keys regularly
- Revoke keys when no longer needed

### Self-hosted Instances

For self-hosted Outline instances, replace the base URL:
```bash
# Replace app.getoutline.com with your domain
curl https://your-outline-instance.com/api/documents.list \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  ...
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using GET requests | Outline API only accepts POST requests |
| Missing Content-Type header | Always include `Content-Type: application/json` |
| Hardcoding API keys | Use environment variables or secure config |
| Ignoring pagination | Use `nextPath` for efficient pagination |
| Not handling 429 errors | Implement rate limit handling with backoff |

## CLI Usage Example

Create a helper script for common operations:

```bash
#!/bin/bash
# outline.sh - Outline CLI helper

OUTLINE_API_BASE="${OUTLINE_API_BASE:-https://app.getoutline.com}"
OUTLINE_API_KEY="${OUTLINE_API_KEY:?Error: OUTLINE_API_KEY not set}"

outline_request() {
  local method="$1"
  local data="$2"

  curl -s "${OUTLINE_API_BASE}/api/${method}" \
    -X 'POST' \
    -H "authorization: Bearer ${OUTLINE_API_KEY}" \
    -H 'content-type: application/json' \
    -H 'accept: application/json' \
    -d "${data}"
}

# Usage examples:
# outline_request "documents.list" '{"limit": 50}'
# outline_request "documents.info" '{"id": "doc_id"}'
# outline_request "documents.search" '{"query": "search term"}'
```

## Additional Resources

- Official documentation: https://www.getoutline.com/developers
- OpenAPI specification: Available for generating clients
- Community: GitHub discussions and issues

**Remember:** Outline's API is RPC-style - all methods are POST requests to `/api/:method` with JSON payloads.
