# Test report (Windows, Git Bash)

- Tester: Nazrin Baghirova
- Date: 2026-11-23
- Environment: Windows, Git Bash, Python 3.14.4, venv
- Code tested: `main` branch, commit 7bf8873
- Method: HTTP requests sent with `curl` from Git Bash

## Setup check

- Clone, `py -m venv venv`, activate and `pip install -r requirements.txt` finished without errors.
- `uvloop` is skipped automatically on Windows, install is clean.
- Greeting page and Swagger docs (`/docs`) open in the browser.

## Results

| # | Request | Expected | Actual |
|---|---|---|---|
| 1 | GET /health | 200 | 200 |
| 2 | GET /api/v1/interviews (User A, own list) | 200 | 200 |
| 3 | GET /api/v1/interviews (no token) | 401 | 401 |
| 4 | GET /api/v1/interviews/interview_1 (own) | 200 | 200 |
| 5 | User A reads User B's interview_3 | 404 | 404 |
| 6 | GET non-existent interview | 404 | 404 |
| 7 | Admin reads interview_3 | 200 | 200 |
| 8 | POST valid body | 201 | 201 |
| 9 | POST too short fields | 400 | 400 |
| 10 | GET newly created interview | 200 | 200 |
| 11 | PUT newly created interview | 200 | 200 |
| 12 | PUT completed interview_1 | 409 | 409 |
| 13 | User A updates User B's interview_3 | 404 | 404 |
| 14 | DELETE newly created interview | 200 | 200 |
| 15 | DELETE the same interview again | 404 | 404 |

All 15 requests returned the expected status code.
Issues found: none.
