# ExamFlow — Online Examination Platform

ExamFlow is a web-based examination platform built using FastAPI, Python, SQLite, HTML, CSS, and JavaScript. It provides separate student and administrator portals for conducting examinations, evaluating answers, and tracking results.

## Project Preview

<!-- Add your project screenshot below -->

<p align="center">
  <img src="screenshots/dashboard.png" alt="ExamFlow Dashboard" width="850">
</p>

## Features

### Student Portal
- Student login and personalized dashboard.
- Browse 10 preloaded examinations with 5 questions each.
- Timed examinations with question navigation.
- Automatic answer evaluation and score calculation.
- View results, scores, and answer reviews.
- Track previous examination attempts.

### Admin Portal
- Separate administrator login and dashboard.
- View examination and submission statistics.
- Create examinations with multiple-choice questions.
- Configure examination duration.
- Publish or hide examinations.
- View student submissions and results.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | Token-based authentication |
| API Documentation | Swagger UI / OpenAPI |
| Server | Uvicorn |

## System Architecture

```text
Student / Administrator
          |
          v
    Web Interface
   HTML, CSS, JS
          |
          v
    FastAPI Backend
          |
    +-----+------+
    |            |
    v            v
Authentication  Exam & Result
                 Management
          |
          v
     SQLite Database
          |
          v
  Scores and Results
```

## Project Structure

```text
exam_platform/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── security.py
│   ├── seed.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.10 or later
- pip
- A modern web browser

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

**2. Create and activate a virtual environment**

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the application**

```bash
uvicorn app.main:app --reload
```

**5. Open the application**

| Resource | URL |
|---|---|
| Web Application | http://127.0.0.1:8000 |
| API Documentation | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/api/health |

The frontend is served directly by FastAPI, so a separate frontend server is not required.

## Demo Credentials

| Role | Email | Password |
|---|---|---|
| Student | `student@examflow.demo` | `Student@123` |
| Admin | `admin@examflow.demo` | `Admin@123` |

These credentials are intended for local demonstration only. Change them before any public deployment.

## REST API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/login` | User authentication |
| GET | `/api/auth/me` | Get current user |
| GET | `/api/exams` | List available examinations |
| GET | `/api/exams/{exam_id}` | Get examination details |
| POST | `/api/exams/{exam_id}/start` | Start an examination |
| GET | `/api/attempts/{attempt_id}/questions` | Retrieve questions |
| POST | `/api/attempts/{attempt_id}/submit` | Submit and evaluate answers |
| GET | `/api/results` | View examination results |
| GET | `/api/admin/dashboard` | View admin statistics |
| POST | `/api/admin/exams` | Create an examination |
| PATCH | `/api/admin/exams/{exam_id}` | Update publication status |
| GET | `/api/admin/submissions` | View student submissions |

Explore request parameters and response schemas at `/docs`.

## Database Design

The application uses SQLite and SQLAlchemy to manage the following entities:

- **Users:** Student and administrator accounts.
- **Exams:** Examination details and duration.
- **Questions:** Questions, answer options, and correct answers.
- **Attempts:** Selected answers, scores, and submission timestamps.

## System Design Concepts

- REST API design and HTTP methods.
- Role-based access control.
- Relational database modeling.
- Request validation and error handling.
- Server-side evaluation and score calculation.
- Examination submission and result workflows.
- Foundations for scalable, distributed examination systems.

## Future Enhancements

- PostgreSQL for production database management.
- Redis caching and shared session management.
- Message queues for asynchronous evaluation and notifications.
- Load balancing and horizontal scaling.
- Exam scheduling and randomized questions.
- Email notifications and result exports.
- Automated testing and Docker deployment.

The current version is a functional demonstration. Supporting millions of simultaneous students would require additional distributed infrastructure, security improvements, and load testing.

---

**Developed using Python, FastAPI, SQLite, HTML, CSS, and JavaScript.**
