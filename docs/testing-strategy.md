# Testing Strategy

## Overview

This project is a FastAPI-based REST API for managing users, projects, and tasks. It includes authentication, authorization, validation, workflow rules, and automated API testing using pytest.

The goal of the test suite is to verify that endpoints respond correctly and also that the system enforces business rules, protects user boundaries, and handles invalid input safely.

---

## Testing Goals

The test suite is designed to validate the following quality areas:

- Core API functionality
- Input validation
- Authentication behavior
- Authorization and ownership rules
- Resource relationships
- Workflow/state transition logic
- Data integrity rules
- Regression protection for future changes

---

## Test Types

### Smoke Tests

Smoke tests cover the most important happy-path flows in the application. 

Examples of smoke coverage include:

- create user
- get users with valid authentication
- create project
- create task
- valid task status transition

Smoke tests are designed to be fast.

---

### Regression Tests

Regression tests cover broader system behavior, especially edge cases, validation rules, and negative scenarios.

Examples of regression coverage include:

- invalid user/project/task input
- missing or invalid API key
- duplicate project names for the same user
- duplicate task titles in the same project
- unauthorized access to another user's resources
- invalid task workflow transitions
- lifecycle and delete scenarios

Regression tests are intended to catch unintended side effects when the application evolves.

---

## Test Scope by Risk Area

### 1. Validation

The test suite verifies that the API rejects invalid input such as:

- missing required fields
- too-short values
- whitespace-only names/titles
- invalid task status values

This helps protect data quality and ensures the API does not accept meaningless or malformed content.

---

### 2. Authentication

The test suite verifies that protected endpoints require a valid API key.

Covered scenarios include:

- missing API key
- invalid API key
- valid API key access

This confirms that only authenticated requests can access protected functionality.

---

### 3. Authorization

The test suite verifies that users can only access their own resources.

Covered scenarios include:

- a user accessing their own projects/tasks
- a different user attempting to access another user's project
- a different user attempting to create tasks in another user's project

This protects resource boundaries and simulates real-world access control testing.

---

### 4. Resource Relationships

The application models dependent resources:

- users own projects
- projects contain tasks

The test suite verifies that:

- projects cannot be used unless the user is valid
- tasks cannot be created without a valid project
- task access is indirectly controlled through project ownership

This ensures that the API correctly enforces parent-child relationships.

---

### 5. Workflow Rules

Task status changes are governed by transition rules.

Current valid transitions are:

- `todo -> in_progress`
- `in_progress -> done`

An Invalid transitions return `409 Conflict`.

The test suite verifies both valid and invalid transitions.

---

### 6. Data Integrity Rules

The application includes scoped uniqueness rules:

- project names must be unique per user
- task titles must be unique within a project

The test suite verifies both the failing cases and the allowed cases where the same names are used in different scopes.

This helps ensure that validation rules are not too weak or too broad.

---

## Test Design Approach

### Fixtures

Fixtures are used to provide:

- shared API client setup
- automatic in-memory database reset before each test
- reusable authenticated user setup

This supports test isolation and repeatability.

---

### Helpers

Reusable helper functions reduce repeated setup logic for:

- creating users
- building auth headers
- creating projects
- creating tasks

This improves readability and maintainability of the test suite.

---

### Parametrization

Parametrized tests are used where multiple inputs should produce the same kind of result, such as invalid user name cases.

This improves test clarity while reducing duplication.

---

## Test Isolation

The application uses in-memory storage, so test isolation is critical.

An autouse fixture clears all in-memory data structures before each test:

- `users_db`
- `projects_db`
- `tasks_db`

This ensures that tests do not leak state into one another and remain deterministic.

---

## CI/CD Validation

The test suite is executed automatically in GitHub Actions on push and pull request events.

The CI pipeline currently performs the following:

- installs dependencies
- runs the pytest suite
- checks code coverage
- enforces a minimum coverage threshold
- generates an HTML test report artifact

This ensures that quality checks are applied consistently outside the local environment.

---

## Out of Scope / Current Limitations

The current test strategy does not yet cover:

- database-backed persistence
- load or performance testing
- role-based authorization
- JWT authentication
- browser/UI automation
- contract testing against an external specification

These are planned as future improvements.

---

## Future Enhancements

Potential next steps for expanding the testing strategy include:

- move from in-memory storage to SQLite or PostgreSQL
- add role-based authorization scenarios
- introduce JWT authentication tests
- add pagination and filtering coverage
- separate CI smoke and regression execution paths
- add linting/static analysis checks in CI
- expand reporting and documentation

---

## Summary

This testing strategy is designed to demonstrate practical QA automation skills beyond basic endpoint checks. The suite validates functionality, security boundaries, workflow behavior, and data integrity while remaining maintainable through fixtures, helpers, and structured test organization.