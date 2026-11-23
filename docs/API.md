# Intervia API Documentation (v1)

Base URL: `http://127.0.0.1:8000`

## 1. Overview

The API is resource-oriented. The main resource is **interviews** (a candidate's practice interview session). Data is mocked in memory and resets when the server restarts.

### Authentication

Send a mock token in every protected request:

```http
Authorization: Bearer user-a-token
```

| Role | Token | Permissions |
|---|---|---|
| Regular user A | `user-a-token` | Manages only own interviews |
| Regular user B | `user-b-token` | Manages only own interviews |
| Administrator | `admin-token` | Manages all interviews |

### Response format

Success:

```json
{ "success": true, "message": "Interview created successfully.", "data": { }, "meta": { } }
```

`meta` (`total`, `page`, `perPage`) appears only in list responses. `data` is `null` for delete.

Error:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid or missing fields.",
    "details": [ { "field": "jobTitle", "message": "String should have at least 3 characters" } ]
  }
}
```

`details` appears only for validation errors. Errors never expose stack traces, paths or internals.

### Error codes

| HTTP | `error.code` | Meaning |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Invalid or missing fields, wrong types, unknown fields, bad query parameters |
| 401 | `UNAUTHORIZED` | Token missing or invalid |
| 403 | `FORBIDDEN` | Reserved (not used, see design decision below) |
| 404 | `NOT_FOUND` | Resource does not exist or belongs to another user |
| 405 | `METHOD_NOT_ALLOWED` | HTTP method not supported for the endpoint |
| 409 | `CONFLICT` | Request conflicts with current state |
| 500 | `INTERNAL_ERROR` | Unexpected server error (generic message) |

### Design decision: 404 instead of 403

When a regular user requests another user's interview, the API returns **404 Not Found**, not 403. Interviews contain private answers and feedback; a 403 would confirm that the ID exists. Returning 404 hides its existence. The administrator can access every interview.

## 2. Interview object

| Field | Type | Notes |
|---|---|---|
| `id` | string | e.g. `interview_1` |
| `ownerId` | string | `user-a`, `user-b` |
| `jobTitle` | string | 3-100 characters |
| `jobDescription` | string | 10-2000 characters |
| `mode` | string | `text` or `voice` |
| `status` | string | `ready`, `in_progress`, `completed` |
| `score` | integer or null | 0-100 |
| `createdAt` | string | ISO 8601 UTC |

## 3. Endpoints

### 3.1 List interviews

`GET /api/v1/interviews`

- **Headers:** `Authorization: Bearer <token>` (any role)
- **Query:** `page` (int, >=1, default 1), `perPage` (int, 1-100, default 10), `status` (`ready` | `in_progress` | `completed`, optional)
- **Behaviour:** regular users see only their own interviews; admin sees all.
- **Success:** `200 OK`, `data` is an array, `meta` has `total`, `page`, `perPage`.
- **Errors:** `401 UNAUTHORIZED`, `400 VALIDATION_ERROR` (e.g. `page=0`, `status=wrong`).

Example:

```bash
curl -H "Authorization: Bearer user-a-token" "http://127.0.0.1:8000/api/v1/interviews?status=ready"
```

```json
{
  "success": true,
  "message": "Interviews retrieved successfully.",
  "data": [
    { "id": "interview_2", "ownerId": "user-a", "jobTitle": "Data Analyst",
      "jobDescription": "SQL and dashboards for a retail company.", "mode": "voice",
      "status": "ready", "score": null, "createdAt": "2026-11-05T12:30:00Z" }
  ],
  "meta": { "total": 1, "page": 1, "perPage": 10 }
}
```

### 3.2 Get one interview

`GET /api/v1/interviews/{id}`

- **Headers:** `Authorization: Bearer <token>`
- **Path:** `id` (string)
- **Success:** `200 OK`
- **Errors:** `401 UNAUTHORIZED`, `404 NOT_FOUND` (missing ID or another user's interview).

Example (User A requests User B's interview):

```bash
curl -i -H "Authorization: Bearer user-a-token" http://127.0.0.1:8000/api/v1/interviews/interview_3
```

```json
{ "success": false, "error": { "code": "NOT_FOUND", "message": "Interview not found." } }
```

### 3.3 Create interview

`POST /api/v1/interviews`

- **Headers:** `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Body:**

| Field | Type | Required | Rules |
|---|---|---|---|
| `jobTitle` | string | yes | 3-100 chars |
| `jobDescription` | string | yes | 10-2000 chars |
| `mode` | string | no | `text` (default) or `voice` |

Unknown fields are rejected. `ownerId` is taken from the token; `status` starts as `ready`.

- **Success:** `201 Created` with `Location: /api/v1/interviews/{id}` header.
- **Errors:** `401 UNAUTHORIZED`, `400 VALIDATION_ERROR`.

Example:

```bash
curl -X POST -H "Authorization: Bearer user-a-token" -H "Content-Type: application/json" \
  -d '{"jobTitle":"QA Intern","jobDescription":"Testing web applications"}' \
  http://127.0.0.1:8000/api/v1/interviews
```

```json
{
  "success": true,
  "message": "Interview created successfully.",
  "data": { "id": "interview_5", "ownerId": "user-a", "jobTitle": "QA Intern",
            "jobDescription": "Testing web applications", "mode": "text",
            "status": "ready", "score": null, "createdAt": "2026-11-22T20:55:44Z" }
}
```

Validation error example (`{"jobTitle":"","extra":1}`): `400`

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid or missing fields.",
    "details": [
      { "field": "jobTitle", "message": "String should have at least 3 characters" },
      { "field": "jobDescription", "message": "Field required" },
      { "field": "extra", "message": "Extra inputs are not permitted" }
    ]
  }
}
```

### 3.4 Update interview

`PUT /api/v1/interviews/{id}`

- **Headers:** `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Body (all required):** `jobTitle`, `jobDescription`, `mode`, `status` (`ready` | `in_progress` | `completed`), `score` (integer 0-100 or null). Same length rules as create; unknown fields rejected.
- **Success:** `200 OK`
- **Errors:** `401 UNAUTHORIZED`, `404 NOT_FOUND`, `400 VALIDATION_ERROR`, `409 CONFLICT` (interview is already `completed` and cannot be modified).

Example:

```bash
curl -X PUT -H "Authorization: Bearer user-a-token" -H "Content-Type: application/json" \
  -d '{"jobTitle":"Senior Analyst","jobDescription":"SQL and dashboards","mode":"text","status":"in_progress","score":null}' \
  http://127.0.0.1:8000/api/v1/interviews/interview_2
```

Conflict example (`interview_1` is completed): `409`

```json
{ "success": false, "error": { "code": "CONFLICT", "message": "A completed interview cannot be modified." } }
```

### 3.5 Delete interview

`DELETE /api/v1/interviews/{id}`

- **Headers:** `Authorization: Bearer <token>`
- **Success:** `200 OK`, `data` is `null`.
- **Errors:** `401 UNAUTHORIZED`, `404 NOT_FOUND`.

```json
{ "success": true, "message": "Interview deleted successfully.", "data": null }
```

### 3.6 Other endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/greeting` | HTML page: project, team, endpoints, status (public, `text/html; charset=utf-8`) |
| GET | `/health` | Health check (public) |
| GET | `/api/v1/me` | Returns the user for the current token (`401` if invalid) |

Unsupported methods on any route return `405 METHOD_NOT_ALLOWED`.

## 4. Mock data

| ID | Owner | Status |
|---|---|---|
| `interview_1` | user-a | completed |
| `interview_2` | user-a | ready |
| `interview_3` | user-b | in_progress |
| `interview_4` | user-b | completed |
| `interview_999` | (does not exist) | used to demo `404` |