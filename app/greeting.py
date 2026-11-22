from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["greeting"])

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Intervia API</title>
  <style>
    :root { --bg:#f4f6fb; --card:#ffffff; --text:#1f2937; --muted:#6b7280; --accent:#4f46e5; --border:#e5e7eb; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }
    header { background:var(--accent); color:#fff; padding:40px 20px; text-align:center; }
    header h1 { margin:0 0 8px; font-size:2rem; }
    header p { margin:0 auto; max-width:640px; opacity:.95; }
    main { max-width:900px; margin:0 auto; padding:24px 16px 48px; }
    section { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:20px; }
    h2 { margin-top:0; font-size:1.25rem; color:var(--accent); }
    .status { display:flex; flex-wrap:wrap; gap:12px; align-items:center; }
    .badge { display:inline-block; padding:4px 12px; border-radius:999px; font-size:.85rem; font-weight:600; }
    .ok { background:#dcfce7; color:#166534; }
    .ver { background:#e0e7ff; color:#3730a3; }
    .team { display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:16px; }
    .member { border:1px solid var(--border); border-radius:10px; padding:14px; }
    .member h3 { margin:0; font-size:1.05rem; }
    .member .id { color:var(--muted); font-size:.9rem; margin-bottom:6px; }
    .table-wrap { overflow-x:auto; }
    table { width:100%; border-collapse:collapse; min-width:560px; }
    th, td { text-align:left; padding:10px 8px; border-bottom:1px solid var(--border); font-size:.95rem; vertical-align:top; }
    th { color:var(--muted); font-weight:600; }
    code { font-family: ui-monospace, Menlo, Consolas, monospace; background:#f3f4f6; padding:2px 6px; border-radius:6px; font-size:.9rem; }
    .m { font-weight:700; }
    .GET { color:#047857; } .POST { color:#1d4ed8; } .PUT { color:#b45309; } .DELETE { color:#b91c1c; }
    footer { text-align:center; color:var(--muted); font-size:.85rem; padding-bottom:24px; }
    @media (max-width:600px) { header h1 { font-size:1.5rem; } header { padding:28px 16px; } }
  </style>
</head>
<body>
  <header>
    <h1>Welcome to Intervia</h1>
    <p>Intervia is an AI-powered interview preparation platform. Candidates upload a CV and a job description, practice tailored interview questions by voice or text, and receive feedback on their answers. It is built for university students, job seekers, career centers and HR professionals.</p>
  </header>
  <main>
    <section>
      <h2>Status</h2>
      <div class="status">
        <span class="badge ok">API is running</span>
        <span class="badge ver">Version v1</span>
        <span>Mock data is stored in memory and resets when the server restarts.</span>
      </div>
    </section>

    <section>
      <h2>Team</h2>
      <div class="team">
        <div class="member">
          <h3>Gular Sultanli</h3>
          <div class="id">Student ID: 20418</div>
          <div>Project setup, token authentication, role and ownership checks, interviews CRUD, validation, response envelope and error handling.</div>
        </div>
        <div class="member">
          <h3>Nazrin Baghirova</h3>
          <div class="id">Student ID: 20025</div>
          <div>Windows compatibility fix, environment testing, and project documentation.</div>
        </div>
      </div>
    </section>

    <section>
      <h2>Available endpoints</h2>
      <p>Protected endpoints need the header <code>Authorization: Bearer &lt;token&gt;</code> (<code>user-a-token</code>, <code>user-b-token</code> or <code>admin-token</code>).</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Method</th><th>Path</th><th>Description</th></tr></thead>
          <tbody>
            <tr><td class="m GET">GET</td><td><code>/api/v1/greeting</code></td><td>This page (public, HTML).</td></tr>
            <tr><td class="m GET">GET</td><td><code>/health</code></td><td>Health check (public).</td></tr>
            <tr><td class="m GET">GET</td><td><code>/api/v1/me</code></td><td>Returns the user for the current token.</td></tr>
            <tr><td class="m GET">GET</td><td><code>/api/v1/interviews</code></td><td>List interviews (own; admin sees all). Supports page, perPage, status.</td></tr>
            <tr><td class="m GET">GET</td><td><code>/api/v1/interviews/{id}</code></td><td>Get one interview.</td></tr>
            <tr><td class="m POST">POST</td><td><code>/api/v1/interviews</code></td><td>Create an interview.</td></tr>
            <tr><td class="m PUT">PUT</td><td><code>/api/v1/interviews/{id}</code></td><td>Update an interview.</td></tr>
            <tr><td class="m DELETE">DELETE</td><td><code>/api/v1/interviews/{id}</code></td><td>Delete an interview.</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
  <footer>CSCI 3509 &middot; Team 2 &middot; Intervia API v1</footer>
</body>
</html>
"""


@router.get("/api/v1/greeting", response_class=HTMLResponse)
def greeting():
    return HTMLResponse(content=PAGE, media_type="text/html; charset=utf-8")