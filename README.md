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
- Lints code with Flake8
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

### Documentation

[Testing Strategy] (docx/testing-strategy.md)