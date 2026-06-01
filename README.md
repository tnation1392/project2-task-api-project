 # Project2 Task API Project

![CI](https://github.com/YOUR_USERNAME/project2-task-api-project/actions/workflows/ci.yml/badge.svg)

A REST API built with FastAPI that manages users, projects, and tasks, combined with a comprehensive pytest-based QA automation suite and CI/CD pipeline. This project demonstrates real-world API testing, authentication, authorization, and automated quality enforcement.

---

## Features

### API Functionality
- Users, Projects, and Tasks resources
- Full CRUD operations
- In-memory data storage (no database required)
- Input validation using Pydantic
- RESTful API design principles

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

### Run locally:

bash
pytest --html=report.html --self-contained-html

### Documentation

[Testing Strategy] (docx/testing-strategy.md)