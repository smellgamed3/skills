---
name: outline-cli
description: Use when the user wants to interact with Outline (the wiki and knowledge base app) via API — including creating, reading, updating, deleting, searching, archiving, moving, or duplicating documents; managing collections, comments, users, groups, shares, stars, templates, revisions, attachments, file operations, events, or data attributes; or checking authentication. Supports API keys and OAuth. Works with both cloud (app.getoutline.com) and self-hosted instances.
---

# Outline API Skill

## Overview

Outline is a modern wiki and knowledge base with a comprehensive RPC-style API. Every endpoint is a `POST` request to `https://app.getoutline.com/api/:method` (or your self-hosted domain). All request bodies and response bodies are JSON.

**Environment variables (set before use):**
```bash
export OUTLINE_API_KEY="ol_api_..."          # required
export OUTLINE_API_BASE="https://app.getoutline.com"  # or your self-hosted URL
```

**Reusable helper function (bash):**
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

## Decision Tree

```
What do you need to do?
│
├─ Work with documents?              → documents.*
├─ Manage collections?               → collections.*
├─ Add/read comments?                → comments.*
├─ Manage users?                     → users.*
├─ Manage groups?                    → groups.*
├─ Share documents publicly?         → shares.*
├─ Star/favorite items?              → stars.*
├─ View document revisions/history?  → revisions.*
├─ Work with templates?              → templates.*
├─ Upload/manage file attachments?   → attachments.*
├─ Import/export bulk data?          → collections.export* / fileOperations.*
├─ Audit trail / activity stream?    → events.list
├─ Custom metadata fields?           → dataAttributes.* (Business/Enterprise)
└─ Check API auth / workspace info?  → auth.*
```

---

## Authentication

| Method | Description |
|--------|-------------|
| **API Key** | `Authorization: Bearer ol_api_<38 chars>`. Create under **Settings → API & Apps**. |
| **OAuth 2.0** | Register app under **Settings → Applications**, then exchange credentials for an access token. |

**Scopes** (restrict API key access):

| Scope | Access granted |
|-------|----------------|
| `read` | All read actions |
| `write` | All read + write actions |
| `documents:read` | Document reads only |
| `documents:write` | Document reads + writes |
| `collections:read` | Collection reads only |
| `collections:write` | Collection reads + writes |
| `documents.*` | All document API methods |
| `users.*` | All user API methods |

---

## Response Envelope

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
  "ok": true, "data": [...],
  "pagination": { "limit": 25, "offset": 0, "nextPath": "/api/documents.list?limit=25&offset=25" }
}
```

Pagination parameters accepted by all list endpoints: `limit` (default 25), `offset`.  
Sorting parameters: `sort` (field name), `direction` (`ASC` | `DESC`).

---

## Auth

### `auth.info` — Retrieve current auth details
```bash
outline auth.info
```
Returns the current user and team associated with the API key.

### `auth.config` — Retrieve authentication options (public, no auth required)
```bash
outline auth.config
```
Returns available authentication providers (SSO services) for a workspace.

---

## Documents

### `documents.info` — Retrieve a document
```bash
outline documents.info '{"id": "DOC_ID_OR_URL_ID"}'
# Or by share ID:
outline documents.info '{"shareId": "SHARE_UUID"}'
```

### `documents.list` — List all published documents
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

### `documents.drafts` — List current user's draft documents
```bash
outline documents.drafts '{
  "collectionId": "COLLECTION_UUID",   // optional
  "dateFilter": "week",                // optional: day | week | month | year
  "limit": 25, "offset": 0
}'
```

### `documents.archived` — List archived documents
```bash
outline documents.archived '{"collectionId": "COLLECTION_UUID", "limit": 25}'
```

### `documents.deleted` — List deleted (trashed) documents
```bash
outline documents.deleted '{"limit": 25, "offset": 0}'
```

### `documents.viewed` — List recently viewed documents
```bash
outline documents.viewed '{"limit": 25}'
```

### `documents.documents` — Get a document's child structure (tree)
```bash
outline documents.documents '{"id": "DOC_ID"}'
```

### `documents.search` — Full-text search across documents
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
Returns array of `{ context, ranking, document }`.

### `documents.search_titles` — Search document titles only (faster)
```bash
outline documents.search_titles '{
  "query": "API guide",
  "collectionId": "COLLECTION_UUID",
  "statusFilter": ["published"],
  "limit": 25
}'
```

### `documents.answerQuestion` — AI-powered Q&A over documents *(Business/Enterprise/Cloud)*
```bash
outline documents.answerQuestion '{
  "query": "What is our holiday policy?",
  "collectionId": "COLLECTION_UUID"
}'
```

### `documents.create` — Create a document
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

### `documents.update` — Update a document
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

### `documents.duplicate` — Duplicate a document
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

### `documents.move` — Move a document
```bash
outline documents.move '{
  "id": "DOC_ID",
  "collectionId": "TARGET_COLLECTION_UUID",
  "parentDocumentId": "NEW_PARENT_UUID",  // omit = collection root
  "index": 0                              // optional: position in list
}'
```

### `documents.archive` — Archive a document
```bash
outline documents.archive '{"id": "DOC_ID"}'
```

### `documents.restore` — Restore an archived or deleted document
```bash
outline documents.restore '{
  "id": "DOC_ID",
  "collectionId": "COLLECTION_UUID",  // optional: restore to specific collection
  "revisionId":   "REVISION_UUID"     // optional: restore to a past revision
}'
```

### `documents.unpublish` — Move a published document back to draft
```bash
outline documents.unpublish '{"id": "DOC_ID", "detach": false}'
```

### `documents.delete` — Delete a document (moves to trash)
```bash
outline documents.delete '{"id": "DOC_ID"}'
# Permanently destroy (no recovery):
outline documents.delete '{"id": "DOC_ID", "permanent": true}'
```

### `documents.export` — Export a document as Markdown/HTML/PDF
```bash
# Markdown (default Accept header):
outline documents.export '{"id": "DOC_ID"}'
# Include child documents (returns zip):
outline documents.export '{"id": "DOC_ID", "includeChildDocuments": true}'
# PDF with specific paper size:
outline documents.export '{"id": "DOC_ID", "paperSize": "A4"}'
```

### `documents.import` — Import a file as a document
```bash
curl -sf "${OUTLINE_API_BASE}/api/documents.import" \
  -X POST \
  -H "Authorization: Bearer ${OUTLINE_API_KEY}" \
  -F "file=@/path/to/file.md" \
  -F "collectionId=COLLECTION_UUID" \
  -F "publish=true"
```
Supported file types: plain text, Markdown, DOCX, CSV, TSV, HTML.

### `documents.templatize` — Create a template from a document
```bash
outline documents.templatize '{
  "id": "DOC_ID",
  "collectionId": "COLLECTION_UUID",
  "publish": true
}'
```

### `documents.users` — List all users with access to a document
```bash
outline documents.users '{"id": "DOC_ID", "query": "alice"}'
```

### `documents.memberships` — List users with direct membership on a document
```bash
outline documents.memberships '{"id": "DOC_ID", "permission": "read"}'
```

### `documents.add_user` — Grant a user access to a document
```bash
outline documents.add_user '{"id": "DOC_ID", "userId": "USER_UUID", "permission": "read"}'
```

### `documents.remove_user` — Revoke a user's access to a document
```bash
outline documents.remove_user '{"id": "DOC_ID", "userId": "USER_UUID"}'
```

### `documents.add_group` — Grant a group access to a document
```bash
outline documents.add_group '{"id": "DOC_ID", "groupId": "GROUP_UUID", "permission": "read"}'
```

### `documents.remove_group` — Revoke a group's access to a document
```bash
outline documents.remove_group '{"id": "DOC_ID", "groupId": "GROUP_UUID"}'
```

---

## Collections

### `collections.info` — Retrieve a collection
```bash
outline collections.info '{"id": "COLLECTION_UUID"}'
```

### `collections.list` — List all collections
```bash
outline collections.list '{
  "query": "engineering",
  "statusFilter": ["active"],
  "limit": 25, "offset": 0
}'
```

### `collections.documents` — Get a collection's full document tree
```bash
outline collections.documents '{"id": "COLLECTION_UUID"}'
```
Returns a nested tree of navigation nodes.

### `collections.create` — Create a collection
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

### `collections.update` — Update a collection
```bash
outline collections.update '{
  "id": "COLLECTION_UUID",
  "name": "Engineering (Updated)",
  "description": "Updated description.",
  "permission": "read_write",
  "sharing": false
}'
```

### `collections.delete` — Delete a collection and all its documents
```bash
outline collections.delete '{"id": "COLLECTION_UUID"}'
```
⚠️ Irreversible — deletes all documents inside.

### `collections.export` — Export a collection as a zip
```bash
outline collections.export '{
  "id": "COLLECTION_UUID",
  "format": "outline-markdown"   // outline-markdown | json | html
}'
```
Returns a `FileOperation` — poll `fileOperations.info` for status and download URL.

### `collections.export_all` — Export all collections
```bash
outline collections.export_all '{
  "format": "outline-markdown",
  "includeAttachments": true,
  "includePrivate": true
}'
```

### `collections.memberships` — List individual user memberships
```bash
outline collections.memberships '{
  "id": "COLLECTION_UUID",
  "query": "jenny",
  "permission": "read",
  "limit": 25
}'
```

### `collections.add_user` — Add a user to a collection
```bash
outline collections.add_user '{
  "id": "COLLECTION_UUID",
  "userId": "USER_UUID",
  "permission": "read_write"
}'
```

### `collections.remove_user` — Remove a user from a collection
```bash
outline collections.remove_user '{"id": "COLLECTION_UUID", "userId": "USER_UUID"}'
```

### `collections.group_memberships` — List group memberships on a collection
```bash
outline collections.group_memberships '{"id": "COLLECTION_UUID", "query": "devs"}'
```

### `collections.add_group` — Grant a group access to a collection
```bash
outline collections.add_group '{
  "id": "COLLECTION_UUID",
  "groupId": "GROUP_UUID",
  "permission": "read"
}'
```

### `collections.remove_group` — Revoke a group's access to a collection
```bash
outline collections.remove_group '{"id": "COLLECTION_UUID", "groupId": "GROUP_UUID"}'
```

---

## Comments

### `comments.list` — List comments
```bash
outline comments.list '{
  "documentId": "DOC_UUID",         // optional: filter by document
  "collectionId": "COLLECTION_UUID",// optional: filter by collection
  "includeAnchorText": true,
  "limit": 25, "offset": 0
}'
```

### `comments.info` — Retrieve a single comment
```bash
outline comments.info '{"id": "COMMENT_UUID", "includeAnchorText": true}'
```

### `comments.create` — Create a comment or reply
```bash
outline comments.create '{
  "documentId": "DOC_UUID",
  "text": "This section needs clarification.",
  "parentCommentId": "PARENT_UUID"   // optional: make it a reply
}'
```

### `comments.update` — Update a comment
```bash
outline comments.update '{"id": "COMMENT_UUID", "data": {"text": "Updated text."}}'
```

### `comments.delete` — Delete a comment (and its replies)
```bash
outline comments.delete '{"id": "COMMENT_UUID"}'
```

---

## Users

### `users.info` — Retrieve a user
```bash
outline users.info '{"id": "USER_UUID"}'
```

### `users.list` — List all users in the workspace
```bash
outline users.list '{
  "query": "alice",
  "filter": "active",    // active | suspended | invited | all
  "role": "member",      // admin | member | viewer | guest
  "limit": 25, "offset": 0
}'
```

### `users.update` — Update a user profile
```bash
outline users.update '{"id": "USER_UUID", "name": "Alice Smith", "avatarUrl": "https://..."}'
```

### `users.promote` — Promote a user to admin
```bash
outline users.promote '{"id": "USER_UUID"}'
```

### `users.demote` — Demote an admin to member/viewer
```bash
outline users.demote '{"id": "USER_UUID", "to": "member"}'
```

### `users.suspend` — Suspend a user (revoke access)
```bash
outline users.suspend '{"id": "USER_UUID"}'
```

### `users.activate` — Reactivate a suspended user
```bash
outline users.activate '{"id": "USER_UUID"}'
```

### `users.delete` — Delete a user from the workspace
```bash
outline users.delete '{"id": "USER_UUID"}'
```

---

## Groups

### `groups.info` — Retrieve a group
```bash
outline groups.info '{"id": "GROUP_UUID"}'
```

### `groups.list` — List all groups
```bash
outline groups.list '{"query": "engineering", "limit": 25}'
```

### `groups.create` — Create a group
```bash
outline groups.create '{"name": "Backend Team"}'
```

### `groups.update` — Update a group
```bash
outline groups.update '{"id": "GROUP_UUID", "name": "Backend Engineers"}'
```

### `groups.delete` — Delete a group
```bash
outline groups.delete '{"id": "GROUP_UUID"}'
```

### `groups.memberships` — List users in a group
```bash
outline groups.memberships '{"id": "GROUP_UUID", "query": "bob", "limit": 25}'
```

### `groups.add_user` — Add a user to a group
```bash
outline groups.add_user '{"id": "GROUP_UUID", "userId": "USER_UUID"}'
```

### `groups.remove_user` — Remove a user from a group
```bash
outline groups.remove_user '{"id": "GROUP_UUID", "userId": "USER_UUID"}'
```

---

## Shares

### `shares.info` — Retrieve a share
```bash
outline shares.info '{"id": "SHARE_UUID"}'
# Or by document:
outline shares.info '{"documentId": "DOC_UUID"}'
```

### `shares.list` — List all shares
```bash
outline shares.list '{"limit": 25, "offset": 0}'
```

### `shares.create` — Create a public share link
```bash
outline shares.create '{
  "documentId": "DOC_UUID",
  "published": true,
  "includeChildDocuments": false,
  "urlId": "custom-slug"
}'
```

### `shares.update` — Update share settings
```bash
outline shares.update '{
  "id": "SHARE_UUID",
  "published": false,
  "includeChildDocuments": true
}'
```

### `shares.revoke` — Revoke a share link
```bash
outline shares.revoke '{"id": "SHARE_UUID"}'
```

---

## Stars (Favorites)

### `stars.list` — List starred items
```bash
outline stars.list '{"limit": 25}'
```

### `stars.create` — Star a document or collection
```bash
outline stars.create '{"documentId": "DOC_UUID"}'
outline stars.create '{"collectionId": "COLLECTION_UUID"}'
```

### `stars.delete` — Remove a star
```bash
outline stars.delete '{"id": "STAR_UUID"}'
```

---

## Revisions

### `revisions.info` — Retrieve a specific revision
```bash
outline revisions.info '{"id": "REVISION_UUID"}'
```

### `revisions.list` — List revisions for a document
```bash
outline revisions.list '{"documentId": "DOC_UUID", "limit": 25, "offset": 0}'
```

---

## Templates

### `templates.info` — Retrieve a template
```bash
outline templates.info '{"id": "TEMPLATE_UUID"}'
```

### `templates.list` — List templates
```bash
outline templates.list '{
  "collectionId": "COLLECTION_UUID",  // optional: collection-scoped templates
  "limit": 25
}'
```

### `templates.update` — Update a template
```bash
outline templates.update '{"id": "TEMPLATE_UUID", "title": "New Title", "text": "# Updated"}'
```

### `templates.delete` — Delete a template
```bash
outline templates.delete '{"id": "TEMPLATE_UUID"}'
```

---

## Attachments

### `attachments.create` — Register an attachment and get upload URL
```bash
outline attachments.create '{
  "name": "diagram.png",
  "contentType": "image/png",
  "size": 204800,
  "documentId": "DOC_UUID"   // optional: associate with a document
}'
```
Returns `{ uploadUrl, form, attachment }`. Use the signed `uploadUrl` to PUT the file directly to cloud storage.

### `attachments.redirect` — Get a signed download URL for an attachment
```bash
outline attachments.redirect '{"id": "ATTACHMENT_UUID"}'
```
Returns a `302` redirect to the (possibly signed) file URL.

### `attachments.delete` — Delete an attachment
```bash
outline attachments.delete '{"id": "ATTACHMENT_UUID"}'
```

---

## File Operations (Import / Export Jobs)

File operations are background jobs for bulk imports/exports.

### `fileOperations.info` — Poll a file operation for status
```bash
outline fileOperations.info '{"id": "FILE_OPERATION_UUID"}'
```
Check `data.state`: `creating` → `uploading` → `complete` | `error`.

### `fileOperations.list` — List file operations
```bash
outline fileOperations.list '{"type": "export", "limit": 25}'
```

### `fileOperations.redirect` — Download the output file
```bash
outline fileOperations.redirect '{"id": "FILE_OPERATION_UUID"}'
```
Returns a `302` redirect to the download URL once state is `complete`.

### `fileOperations.delete` — Delete a file operation record
```bash
outline fileOperations.delete '{"id": "FILE_OPERATION_UUID"}'
```

---

## Events (Audit Trail)

### `events.list` — List activity events
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
Useful for audit trails, activity feeds, and monitoring changes.

---

## Data Attributes *(Business/Enterprise only)*

Custom metadata fields that can be attached to documents.

### `dataAttributes.list` — List all data attributes
```bash
outline dataAttributes.list '{"limit": 25}'
```

### `dataAttributes.info` — Retrieve a data attribute
```bash
outline dataAttributes.info '{"id": "DATA_ATTR_UUID"}'
```

### `dataAttributes.create` — Create a data attribute
```bash
outline dataAttributes.create '{
  "name": "Status",
  "description": "Current status of the document.",
  "dataType": "string",   // string | boolean | number | list
  "options": {"values": ["Draft", "Review", "Published"]},
  "pinned": true
}'
```

### `dataAttributes.update` — Update a data attribute
```bash
outline dataAttributes.update '{
  "id": "DATA_ATTR_UUID",
  "name": "Priority",
  "options": {"values": ["Low", "Medium", "High"]},
  "pinned": false
}'
```
Note: `dataType` cannot be changed after creation.

### `dataAttributes.delete` — Delete a data attribute
```bash
outline dataAttributes.delete '{"id": "DATA_ATTR_UUID"}'
```

---

## Complete Endpoint Reference

| Resource | Endpoint | Key Parameters |
|----------|----------|----------------|
| **Auth** | `auth.info` | — |
| | `auth.config` | — (no auth required) |
| **Documents** | `documents.info` | `id` or `shareId` |
| | `documents.list` | `collectionId`, `userId`, `statusFilter`, pagination |
| | `documents.drafts` | `collectionId`, `dateFilter`, pagination |
| | `documents.archived` | `collectionId`, pagination |
| | `documents.deleted` | pagination |
| | `documents.viewed` | pagination |
| | `documents.documents` | `id` |
| | `documents.search` | `query`, filters, pagination |
| | `documents.search_titles` | `query`, filters, pagination |
| | `documents.answerQuestion` ✨ | `query`, `collectionId` |
| | `documents.create` | `title`, `text`, `collectionId`, `publish` |
| | `documents.update` | `id`, `title`, `text`, `publish` |
| | `documents.duplicate` | `id`, `recursive`, `collectionId` |
| | `documents.move` | `id`, `collectionId`, `parentDocumentId` |
| | `documents.archive` | `id` |
| | `documents.restore` | `id`, `collectionId`, `revisionId` |
| | `documents.unpublish` | `id`, `detach` |
| | `documents.delete` | `id`, `permanent` |
| | `documents.export` | `id`, `includeChildDocuments`, `paperSize` |
| | `documents.import` | `file` (multipart), `collectionId`, `publish` |
| | `documents.templatize` | `id`, `collectionId`, `publish` |
| | `documents.users` | `id`, `query` |
| | `documents.memberships` | `id`, `permission` |
| | `documents.add_user` | `id`, `userId`, `permission` |
| | `documents.remove_user` | `id`, `userId` |
| | `documents.add_group` | `id`, `groupId`, `permission` |
| | `documents.remove_group` | `id`, `groupId` |
| **Collections** | `collections.info` | `id` |
| | `collections.list` | `query`, `statusFilter`, pagination |
| | `collections.documents` | `id` |
| | `collections.create` | `name`, `permission`, `icon`, `color` |
| | `collections.update` | `id`, `name`, `permission`, `sharing` |
| | `collections.delete` | `id` |
| | `collections.export` | `id`, `format` |
| | `collections.export_all` | `format`, `includeAttachments` |
| | `collections.memberships` | `id`, `query`, `permission`, pagination |
| | `collections.add_user` | `id`, `userId`, `permission` |
| | `collections.remove_user` | `id`, `userId` |
| | `collections.group_memberships` | `id`, `query`, pagination |
| | `collections.add_group` | `id`, `groupId`, `permission` |
| | `collections.remove_group` | `id`, `groupId` |
| **Comments** | `comments.list` | `documentId`, `collectionId`, pagination |
| | `comments.info` | `id`, `includeAnchorText` |
| | `comments.create` | `documentId`, `text`, `parentCommentId` |
| | `comments.update` | `id`, `data` |
| | `comments.delete` | `id` |
| **Users** | `users.info` | `id` |
| | `users.list` | `query`, `filter`, `role`, pagination |
| | `users.update` | `id`, `name`, `avatarUrl` |
| | `users.promote` | `id` |
| | `users.demote` | `id`, `to` |
| | `users.suspend` | `id` |
| | `users.activate` | `id` |
| | `users.delete` | `id` |
| **Groups** | `groups.info` | `id` |
| | `groups.list` | `query`, pagination |
| | `groups.create` | `name` |
| | `groups.update` | `id`, `name` |
| | `groups.delete` | `id` |
| | `groups.memberships` | `id`, `query`, pagination |
| | `groups.add_user` | `id`, `userId` |
| | `groups.remove_user` | `id`, `userId` |
| **Shares** | `shares.info` | `id` or `documentId` |
| | `shares.list` | pagination |
| | `shares.create` | `documentId`, `published`, `urlId` |
| | `shares.update` | `id`, `published`, `includeChildDocuments` |
| | `shares.revoke` | `id` |
| **Stars** | `stars.list` | pagination |
| | `stars.create` | `documentId` or `collectionId` |
| | `stars.delete` | `id` |
| **Revisions** | `revisions.info` | `id` |
| | `revisions.list` | `documentId`, pagination |
| **Templates** | `templates.info` | `id` |
| | `templates.list` | `collectionId`, pagination |
| | `templates.update` | `id`, `title`, `text` |
| | `templates.delete` | `id` |
| **Attachments** | `attachments.create` | `name`, `contentType`, `size`, `documentId` |
| | `attachments.redirect` | `id` |
| | `attachments.delete` | `id` |
| **File Operations** | `fileOperations.info` | `id` |
| | `fileOperations.list` | `type`, pagination |
| | `fileOperations.redirect` | `id` |
| | `fileOperations.delete` | `id` |
| **Events** | `events.list` | `name`, `documentId`, `userId`, `auditLog`, pagination |
| **DataAttributes** ✨ | `dataAttributes.info` | `id` |
| | `dataAttributes.list` | pagination |
| | `dataAttributes.create` | `name`, `dataType`, `options`, `pinned` |
| | `dataAttributes.update` | `id`, `name`, `options` |
| | `dataAttributes.delete` | `id` |

✨ = Business/Enterprise/Cloud tier required.

---

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| `200` / `201` | Success | — |
| `400` | Validation error | Check request body against required fields |
| `401` | Unauthenticated | Check API key is valid and not revoked |
| `403` | Unauthorized | Check the API key has required scope/permission |
| `404` | Not Found | Verify the resource ID is correct |
| `429` | Rate limited | Wait `Retry-After` seconds, then retry with exponential backoff |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using GET instead of POST | All Outline API endpoints are `POST` |
| Missing `Content-Type: application/json` header | Always include it |
| Hardcoding API keys | Use `OUTLINE_API_KEY` env var |
| Ignoring pagination | Use `nextPath` or increment `offset` by `limit` |
| Not polling `fileOperations.info` after export | Exports are async; poll until `state === "complete"` |
| Forgetting `publish: true` on create | Without it, documents are saved as drafts |
| Permanent delete without intent | Default delete is trash (recoverable); set `permanent: true` to destroy |

---

## Self-hosted Instances

Replace the base URL in all calls:
```bash
export OUTLINE_API_BASE="https://wiki.yourcompany.com"
# Then use the same outline() helper — no other changes needed
```

## Resources

- **Official API docs:** https://www.getoutline.com/developers
- **OpenAPI spec:** https://github.com/outline/openapi
- **API key management:** Settings → API & Apps
- **OAuth app registration:** Settings → Applications
