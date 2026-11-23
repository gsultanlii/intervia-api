
# Intervia API (Assignment 2 prototype)

Intervia is an AI-powered interview preparation platform for students, job seekers, career centers and HR professionals. This repository contains the first backend prototype: a REST API built with FastAPI and **mocked in-memory data** (no real database yet).

Main resource: **interviews** (a candidate's practice interview session).

## Features

- Resource-oriented REST API under `/api/v1/`
- Mock token authentication and role-based authorization (user A, user B, admin)
- Ownership checks: a user cannot read, update or delete another user's interview (returns `404`)
- Validation with structured error responses (`400`, `401`, `404`, `405`, `409`)
- Unified `success` / `error` response envelope
- HTML greeting page at `GET /api/v1/greeting`

## Requirements

- Python 3.10 or newer
- Git

## Install and run

macOS / Linux:

```bash
git clone https://github.com/gsultanlii/intervia-api.git
cd intervia-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows (Git Bash):

```bash
git clone https://github.com/gsultanlii/intervia-api.git
cd intervia-api
py -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows (PowerShell): activate with `venv\Scripts\Activate.ps1`.

The server runs at http://127.0.0.1:8000.

- Greeting page: http://127.0.0.1:8000/api/v1/greeting
- Interactive docs (Swagger): http://127.0.0.1:8000/docs

> **Mock data note:** all data is stored in memory and **resets every time the server restarts**.

## Mock users

| Role | Token |
|---|---|
| User A | `user-a-token` |
| User B | `user-b-token` |
| Administrator | `admin-token` |

Send as: `Authorization: Bearer user-a-token`

## Documentation

- Full API documentation: [docs/API.md](docs/API.md)
- Example requests: [docs/examples.md](docs/examples.md)

## Team

| Name | Student ID | Responsibilities |
|---|---|---|
| Gular Sultanli | 20418 | Project setup, mock data, authentication, ownership checks, interviews CRUD, validation, response envelope, greeting page, API docs |
| Nazrin Baghirova | 20025 | Windows compatibility fix, environment testing, test report(docs/testing.md) |

See [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Git contribution summary

Output of `git shortlog -sn --all`:

```text
    28  Gular Sultanli
    4  Nazrin Baghirova
```