 # Project2 Task API Project

![CI](https://github.com/YOUR_USERNAME/project2-task-api-project/actions/workflows/ci.yml/badge.svg)

A REST API built with FastAPI that manages users, projects, and tasks, combined with a comprehensive pytest-based QA automation suite and CI/CD pipeline. The application uses SQLite with SQLAlchemy for persistent data storage and demonstrates real-world API testing, authentication, authorization, validation, workflow rules, and automated quality enforcement.

---

## Features

### ✅ API Functionality
- Users, Projects, and Tasks resources
- Full CRUD operations
- Persistent data storage using SQLite
- SQLAlchemy ORM for database access
- Input validation using Pydantic
- RESTful API design principles

---

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Testing**: pytest, pytest-asyncio, httpx
- **Coverage**: pytest-cov
- **Reporting**: pytest-html
- **CI/CD**: GitHub Actions
- **Language**: Python 3.11+

---

### Authentication & Authorization
- API key-based authentication
- Ownership-based access control
- Proper HTTP status codes:
  - 401 Unauthorized (missing/invalid API key)
  - 403 Forbidden (access denied)
  - 404 Not Found (resource missing)

### Resource Relationships
- Users own Projects
- Projects contain Tasks
- Nested resource validation and dependency handling

---

## Testing (QA Automation)

This project includes a full pytest-based API automation suite designed to simulate real-world QA testing scenarios.

### Testing Techniques
- Async API testing using `httpx`
- Pytest fixtures for reusable environment setup
- Parametrized tests for validation coverage
- Test isolation using in-memory resets
- Multi-step lifecycle testing (create → update → delete)
- Multi-user testing for access control validation

---

### ✅ CI Pipeline Features
- Installs dependencies
- Checks formatting with Black
- Runs full pytest suite
- Generates code coverage reports
- Enforces minimum coverage (≥ 85%)
- Generates HTML test report
- Uploads report as CI artifact

---

### Coverage Includes
- Positive test cases (happy paths)
- Negative test cases (invalid inputs, auth failures)
- Edge cases (empty values, invalid states)
- Authentication and authorization scenarios
- Resource dependency validation (user → project → task)

---

## Test Reporting

This project generates HTML test reports using `pytest-html`.

### Features
- Visual pass/fail summary
- Detailed test execution output
- Error and stack trace visibility

---

## Contract Testing

The project includes OpenAPI contract validation tests that verify the generated schema remains aligned with the core published API surface.

Current coverage includes:
- OpenAPI schema availability
- OpenAPI version/schema sanity checks
- validation of core resource paths in `/openapi.json`

This helps catch accidental route or API contract regressions early.

---

### Run locally:

bash
pytest --html=report.html --self-contained-html

---

### Database
The application uses a local SQLite database file for persistence.

By default, the database file is created automatically when the application starts:

```bash
task_api.db
```
---

## 🐳 Running with Docker

### Build the image
```bash
docker build -t project2-task-api-project .
### Documentation```
```

--- 

## Docker Status

Docker support was investigated as part of the project roadmap.

### Current local limitation
Local Docker validation is currently blocked on my Windows work environment because:
- Docker Desktop on Windows uses WSL 2 for the recommended per-user installation path
- WSL is not available on this machine
- I do not have administrative permissions to enable/install the required backend

### Project impact
This does not affect the API implementation or the automated test suite when run locally with Python and pytest.

### Planned follow-up
Docker assets can be completed and validated later on:
- a personal machine
- an admin-enabled environment
- or another environment where WSL 2 / Docker Desktop is available

---

## Testing Strategy
(docx/testing-strategy.md)