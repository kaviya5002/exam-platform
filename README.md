# 🎓 ExamFlow — Online Examination Platform

A modern, full-stack online examination platform built with **FastAPI, Python, SQLite, HTML, CSS, and JavaScript**. ExamFlow provides separate student and administrator portals, interactive examinations, automated evaluation, and result tracking through a clean, responsive web interface.

Designed as a practical implementation of low-level and high-level system design concepts, including REST APIs, role-based access, database modeling, and scalable examination workflows.

---

## ✨ Features

### 👨‍🎓 Student Portal
- Secure login with role-based access.
- Personalized student dashboard.
- Browse 10 preloaded examinations across different subjects.
- Attempt multiple-choice examinations with 5 questions per exam.
- Countdown timer for examination sessions.
- Navigate between questions using Previous and Next controls.
- Submit answers for automatic server-side evaluation.
- View scores, percentages, and submission history.
- Review submitted answers alongside correct answers.
- Responsive interface for desktop and mobile screens.

### 🛡️ Administrator Portal
- Separate administrator login and dashboard.
- Monitor students, examinations, published exams, and submissions.
- Create examinations with customizable questions and answer options.
- Configure examination duration.
- Select the correct answer for each question.
- Publish or hide examinations.
- View student submissions and scores.
- Review individual examination results.

### ⚙️ Backend and REST APIs
- FastAPI-powered REST API architecture.
- SQLite database with SQLAlchemy ORM.
- Password hashing for stored credentials.
- Role-based authorization for administrative endpoints.
- Server-side answer evaluation and score calculation.
- Examination attempt and submission tracking.
- Request validation using Pydantic.
- Interactive API documentation with Swagger UI.

---

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | Token-based authentication, password hashing |
| API Documentation | Swagger UI / OpenAPI |
| Development Server | Uvicorn |
| Version Control | Git and GitHub |

---

## 🏗️ System Architecture

```text
                  ┌─────────────────────────┐
                  │       User Interface    │
                  │      HTML, CSS, JS      │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │       FastAPI Backend   │
                  │                         │
                  │  Authentication         │
                  │  Exam Management        │
                  │  Attempt Management     │
                  │  Evaluation & Results   │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │      SQLite Database    │
                  │                         │
                  │  Users                  │
                  │  Exams                  │
                  │  Questions              │
                  │  Attempts & Results     │
                  └─────────────────────────┘
```

### Examination Workflow

```text
Login
  ↓
Role Verification
  ↓
Student: Browse Exams
  ↓
Start Examination
  ↓
Retrieve Questions
  ↓
Select Answers
  ↓
Submit Examination
  ↓
Server-Side Evaluation
  ↓
Calculate Score
  ↓
Store Result
  ↓
Display Result and Answer Review
```

---

## 📁 Project Structure

```text
exam_platform/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and REST endpoints
│   ├── database.py          # Database connection and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── security.py          # Password hashing and verification
│   ├── seed.py              # Demo accounts and initial exam data
│   │
│   └── static/
│       ├── index.html       # Main application interface
│       ├── style.css        # Responsive UI styling
│       └── app.js           # Frontend interactions and API calls
│
├── requirements.txt         # Python dependencies
├── .gitignore               # Git exclusions
└── README.md                # Project documentation
```

The SQLite database is initialized automatically when the application starts for the first time.

---

## 🚀 Getting Started

Follow these steps to run ExamFlow locally.

### Prerequisites

Install the following before starting:

- Python 3.10 or later
- pip
- Git (optional, for cloning the repository)
- A modern web browser

### 1. Clone the Repository

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your GitHub details.

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Navigate into the project directory:

```bash
cd YOUR_REPOSITORY
```

### 2. Create a Virtual Environment

**Windows — PowerShell**

```powershell
py -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python and pip directly using `.venv\Scripts\python.exe` and `.venv\Scripts\pip.exe`.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the Application

```bash
uvicorn app.main:app --reload
```

### 5. Open ExamFlow

| Resource | URL |
|---|---|
| Web Application | http://127.0.0.1:8000 |
| Interactive API Documentation | http://127.0.0.1:8000/docs |
| Alternative API Documentation | http://127.0.0.1:8000/redoc |
| Health Check | http://127.0.0.1:8000/api/health |

The frontend is served by FastAPI, so **you do not need to start a separate frontend development server**.

---

## 🔐 Demo Credentials

Use the following accounts to explore the separate portals.

### Student Account

| Field | Value |
|---|---|
| Email | `student@examflow.demo` |
| Password | `Student@123` |
| Access | Student dashboard, examinations, submissions, and results |

### Administrator Account

| Field | Value |
|---|---|
| Email | `admin@examflow.demo` |
| Password | `Admin@123` |
| Access | Admin dashboard, exam management, and student submissions |

> **Security notice:** These are demonstration credentials. Change or remove them before deploying the application publicly. Never use demo passwords for real accounts.

---

## 🔌 REST API Reference

All application endpoints use the `/api` prefix unless otherwise specified.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login` | Authenticate a user |
| POST | `/api/auth/logout` | Log out the current session |
| GET | `/api/auth/me` | Retrieve the current user's profile |

### Examination Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/exams` | Retrieve available examinations |
| GET | `/api/exams/{exam_id}` | Retrieve examination details |
| POST | `/api/exams/{exam_id}/start` | Start a student examination attempt |
| GET | `/api/attempts/{attempt_id}/questions` | Retrieve questions for an active attempt |
| POST | `/api/attempts/{attempt_id}/submit` | Submit answers and evaluate the attempt |

### Results

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/results` | Retrieve accessible examination results |
| GET | `/api/results/{result_id}` | Retrieve a result and answer review |

### Administrator

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/dashboard` | Retrieve administrative statistics |
| POST | `/api/admin/exams` | Create a new examination |
| PATCH | `/api/admin/exams/{exam_id}` | Update examination publication status |
| GET | `/api/admin/submissions` | Retrieve submitted examination results |

**Authentication:** Protected endpoints require the access token returned by the login endpoint in the `Authorization: Bearer <token>` header.

Explore the complete schemas, parameters, and response formats at `/docs`.

---

## 🗄️ Database Design

ExamFlow uses SQLite for lightweight, local persistence.

### Core Entities

- **Users:** Stores student and administrator accounts, password hashes, and roles.
- **Exams:** Stores examination titles, subjects, descriptions, durations, and publication status.
- **Questions:** Stores question text, answer options, correct answers, and points.
- **Attempts:** Stores the student, examination, attempt status, selected answers, score, and submission timestamp.

### Relationships

```text
User 1 ─────────── * Attempt

Exam 1 ─────────── * Question

Exam 1 ─────────── * Attempt

Attempt ─────────── Result Data
```

The submitted score and answer data are associated with the examination attempt, enabling result history and answer review.

---

## 🧠 System Design Concepts Demonstrated

This project demonstrates practical implementations of:

- RESTful API design and HTTP methods.
- Separation of frontend, backend, and database responsibilities.
- Role-based access control.
- Relational data modeling.
- Request validation and error handling.
- Server-side evaluation and score calculation.
- Examination submission workflows.
- API documentation using OpenAPI.
- Responsive frontend development.
- Foundations for asynchronous evaluation and scalable system architecture.

### HTTP Status Codes

Common status codes used by the application include:

| Code | Meaning |
|---|---|
| `200 OK` | Successful retrieval or operation |
| `201 Created` | Resource creation convention for future API extensions |
| `401 Unauthorized` | Missing or invalid authentication |
| `403 Forbidden` | Insufficient permissions |
| `404 Not Found` | Resource not found |
| `408 Request Timeout` | Examination submission arrived after the allowed duration |
| `409 Conflict` | Attempt already submitted |
| `422 Unprocessable Entity` | Request validation failed |

---

## 📈 Scalability and Future Enhancements

The current implementation is a local demonstration and starting point for a larger online examination platform.

Potential future improvements include:

- PostgreSQL for production-grade relational data storage.
- Redis for caching and shared session or attempt state.
- Background workers and a message queue for asynchronous evaluation and notifications.
- Load balancing and horizontally scaled FastAPI instances.
- WebSocket-based live exam monitoring.
- Email notifications for results and examination reminders.
- Exam scheduling and access windows.
- Randomized question and option ordering.
- Question banks and multiple examination types.
- CSV/PDF result exports.
- Audit logs and administrative reporting.
- Automated unit, integration, and load testing.
- Containerization with Docker and deployment automation.

For a system expected to support millions of concurrent students, the database, authentication, submission processing, caching, and queue infrastructure must be redesigned and validated through load testing. The current project does not claim to support that scale out of the box.

---

## 🔒 Security Considerations

This project is intended for demonstration and educational use.

Before production deployment, implement and validate:

- HTTPS and secure cookie/session handling.
- Persistent, revocable authentication sessions or a suitable identity provider.
- CSRF protection where cookie-based authentication is used.
- Rate limiting and brute-force protection.
- Strict exam timing and server-side deadline enforcement.
- Database migrations, backups, and recovery procedures.
- Audit logging and monitoring.
- Secrets management and environment-based configuration.
- Automated security and concurrency tests.

---

## 🧪 Testing Checklist

Before demonstrating the project, verify the following:

- [ ] Student login works.
- [ ] Administrator login works.
- [ ] Student and administrator permissions are separated.
- [ ] The 10 seeded examinations are visible to students.
- [ ] Each seeded exam contains five questions.
- [ ] Questions and answer choices load correctly.
- [ ] The countdown timer updates during an attempt.
- [ ] Answer selection and question navigation work.
- [ ] Submission calculates the score correctly.
- [ ] Submitted attempts cannot be submitted again.
- [ ] Students can view their own results and answer reviews.
- [ ] Administrators can create and publish examinations.
- [ ] Administrators can hide and republish examinations.
- [ ] API documentation loads at `/docs`.

---

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the updated functionality.
5. Open a pull request with a clear description.

---

## 📄 License

This project is provided for educational and demonstration purposes. Add a `LICENSE` file with your chosen license before distributing it as an open-source project.

---

## 👩‍💻 Project Summary

**ExamFlow** is a FastAPI-based online examination platform that combines a student assessment workflow, administrator exam management, automated scoring, and result tracking in one web application.

It serves as a foundation for exploring backend API development, database design, authentication, and the system architecture required to build larger examination platforms.

**Built with Python, FastAPI, SQLite, HTML, CSS, and JavaScript.**
