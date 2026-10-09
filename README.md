# ExamFlow — Online Examination Platform

A ready-to-run FastAPI + SQLite web application for the Round 2 / Round 3 online examination system design challenge.

## Features
- Responsive web UI with navbar and separate Student/Admin experiences
- Demo login for student and admin; password hashing for seeded accounts
- 10 seeded exams, 5 multiple-choice questions per exam
- Available exams, exam instructions, start exam, timed exam UI, answer selection, submit exam
- Server-side evaluation and results/history
- Admin dashboard with exam statistics, create exam, manage exam visibility, view submissions
- REST API documented at `/docs`
- SQLite database auto-created on first run
- Submission validation: one submission per attempt, active attempt checks, server-side scoring
- Clean separation into API routers, database/models, schemas, services and static frontend

## Run on Windows (PowerShell)
```powershell
cd exam_platform
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Demo accounts
- Student: `student@examflow.demo` / `Student@123`
- Admin: `admin@examflow.demo` / `Admin@123`

Change these credentials before any real deployment.

## API overview
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/exams`
- `GET /api/exams/{exam_id}`
- `POST /api/exams/{exam_id}/start`
- `GET /api/attempts/{attempt_id}/questions`
- `POST /api/attempts/{attempt_id}/submit`
- `GET /api/results`
- `GET /api/results/{result_id}`
- `GET /api/admin/dashboard`
- `POST /api/admin/exams`
- `PATCH /api/admin/exams/{exam_id}`
- `GET /api/admin/submissions`

This is a practical demo/reference implementation. For production, add HTTPS, CSRF protections, robust token/session management, migrations, audit logs, rate limiting, backups, and a proper deployment setup.
