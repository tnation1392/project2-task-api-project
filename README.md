# Project2 Task API Project

[![CI](https://github.com/tnation1392/project2-task-api-project/actions/workflows/ci.yml/badge.svg)](https://github.com/tnation1392/project2-task-api-project/actions/workflows/ci.yml)

A portfolio-quality **FastAPI task management API** with a **QA automation-focused test suite**. The project demonstrates practical API quality engineering through authentication, authorization, validation, filtering, pagination, workflow/state rules, OpenAPI contract testing, and CI quality gates.

---

## Project Overview

This project is designed to showcase **mid-level QA automation skills** through a practical API system built with FastAPI and backed by SQLite + SQLAlchemy.

It combines:
- a working REST API for **Users, Projects, and Tasks**
- a robust **pytest-based automation suite**
- **GitHub Actions CI** for repeatable quality enforcement
- supporting documentation for both implementation and test strategy

---

## API Features

### Core Resources
- Users
- Projects
- Tasks

### Functionality
- Full CRUD support across implemented resources
- SQLite persistence with SQLAlchemy ORM
- Pydantic-based request validation
- Timestamp / audit field coverage
- Filtering support
- Pagination support
- Task workflow/state transition rules

### Security & Authorization
- API key authentication
- Ownership-based authorization
- Role-based authorization:
  - `member`
  - `admin`

### Validation & Business Rules
- Invalid input handling with appropriate HTTP status codes
- Resource ownership enforcement
- Nested resource relationship validation
- Task state transition validation

---

## QA Automation Coverage

This repository is intentionally built as a **QA automation portfolio project**, not just an API demo.

### Test Coverage Includes
- Positive API tests
- Negative API tests
- Edge case scenarios
- Authentication and authorization checks
- Validation rule coverage
- Resource relationship checks
- Filtering and pagination validation
- Task workflow/state transition checks
- OpenAPI contract validation

### Testing Techniques Used
- Async API testing with `httpx`
- `pytest` fixtures for reusable setup
- Parametrized test cases
- Helper / factory-style test setup utilities
- Test isolation between runs
- Smoke and regression markers

### OpenAPI Contract Testing
The project includes OpenAPI contract validation tests against `/openapi.json` to help catch accidental contract regressions.

Current contract checks include:
- OpenAPI schema availability
- OpenAPI version/schema sanity checks
- Core published API paths
- Expected HTTP methods for core resources

---

## Tech Stack

### Application
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

### Testing
- pytest
- pytest-asyncio
- httpx
- pytest-cov
- pytest-html

### Quality / CI
- GitHub Actions
- Black
- Flake8

### Language
- Python 3.11+

---

## Project Structure

```text
project2-task-api-project/
├── app/
├── docs/
│   └── testing-strategy.md
├── tests/
├── .github/
│   └── workflows/
├── README.md
├── requirements.txt
└── ...
```

> Adjust the structure section if your local layout differs slightly.

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/tnation1392/project2-task-api-project.git
cd project2-task-api-project
```

### 2. Create and activate a virtual environment
**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API locally
> Update the module path below if your app entry point differs.

```bash
uvicorn app.main:app --reload
```

### 5. Open the API docs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

---

## Running Tests

### Run the full test suite
```bash
pytest -v
```

### Run smoke tests only
```bash
pytest -m smoke -v
```

### Run regression tests only
```bash
pytest -m regression -v
```

### Run tests with coverage
```bash
pytest --cov=app --cov-report=term-missing
```

### Generate an HTML report
```bash
pytest --html=report.html --self-contained-html
```

---

## CI Quality Gates

The GitHub Actions pipeline is configured to:
- install dependencies
- check formatting with Black
- lint with Flake8
- run the pytest suite
- enforce coverage requirements
- generate and upload HTML test artifacts

This helps keep the project aligned with real-world QA automation and CI expectations.

---

## Database

The application uses a local SQLite database for persistence.

By default, the database file is created automatically when the application starts.

Example database file:
```text
task_api.db
```

---

## Docker Status

Docker support was investigated as part of the project roadmap.

### Current Local Limitation
Local Docker validation is currently blocked in the current Windows work environment because:
- Docker Desktop on Windows uses WSL 2 for the recommended per-user installation path
- WSL is not available on the current machine
- Administrative permissions are not available to enable/install the required backend

### Project Impact
This does **not** affect the API implementation or the automated test suite when running locally with Python and pytest.

### Planned Follow-up
Docker assets can be completed and validated later on:
- a personal machine
- an admin-enabled environment
- or another environment where WSL 2 / Docker Desktop is available

---

## Documentation

Additional documentation:
- `docs/testing-strategy.md`
- `docs/testing-structure.md`'

---

## Roadmap Snapshot

### Completed
- Task state transition rules
- Better validation rules
- Test helpers / factories
- Smoke / regression markers
- Testing strategy document
- SQLite migration / persistence
- Timestamps / audit fields
- Filtering
- Pagination
- Role-based authorization
- Black + Flake8 in CI
- OpenAPI contract testing (paths + methods)

### In Progress / Deferred
- Docker support (blocked locally by environment restrictions)

---

## Why This Project Matters for QA Automation

This project is meant to demonstrate more than endpoint testing. It shows practical QA automation skills such as:
- validating business rules
- testing authorization boundaries
- protecting API contracts
- enforcing quality gates in CI
- documenting test strategy clearly

---

## Future Improvements

Potential next improvements include:
- deeper OpenAPI contract checks (security metadata, schema details)
- Docker validation in an admin-enabled environment
- additional reporting or test organization refinements
- expanded negative and edge-case coverage where useful

---

## Author

Created as a QA automation portfolio project by **Todd Nason**.
