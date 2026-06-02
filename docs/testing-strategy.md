# Testing Strategy

## Overview

This project is a FastAPI-based REST API for managing users, projects, and tasks. It includes authentication, authorization, validation, workflow/state rules, filtering, pagination, SQLite persistence, and automated API testing using pytest.

The goal of the test suite is to verify that endpoints respond correctly and that the system enforces business rules, protects user boundaries, publishes a reliable API contract, and handles invalid input safely.

---

## Testing Goals

The test suite is designed to validate the following quality areas:

- Core API functionality
- Input validation
- Authentication behavior
- Authorization and ownership rules
- Role-based access control
- Resource relationships
- Workflow/state transition logic
- Data integrity rules
- Filtering and pagination behavior
- OpenAPI contract stability
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
- basic authenticated access to protected endpoints

Smoke tests are designed to be fast and provide quick confidence that the core system is functioning.

---

### Regression Tests

Regression tests cover broader system behavior, especially edge cases, validation rules, authorization checks, and negative scenarios.

Examples of regression coverage include:

- invalid user/project/task input
- missing or invalid API key
- duplicate project names for the same user
- duplicate task titles in the same project
- unauthorized access to another user's resources
- invalid task workflow transitions
- filtering and pagination edge cases
- lifecycle and delete scenarios
- OpenAPI contract regressions

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

The test suite verifies that users can only access their own resources unless elevated access rules apply.

Covered scenarios include:

- a user accessing their own projects/tasks
- a different user attempting to access another user's project
- a different user attempting to create tasks in another user's project
- ownership-based access restrictions
- admin vs member authorization behavior

This protects resource boundaries and simulates real-world access control testing.

---

### 4. Role-Based Access Control

The application includes role-aware authorization behavior.

Covered scenarios include:

- standard member access restrictions
- admin-level access where applicable
- validation that role-based rules are enforced consistently

This helps ensure the authorization model remains intentional and testable as the API evolves.

---

### 5. Resource Relationships

The application models dependent resources:

- users own projects
- projects contain tasks

The test suite verifies that:

- projects cannot be used unless the user is valid
- tasks cannot be created without a valid project
- task access is indirectly controlled through project ownership

This ensures that the API correctly enforces parent-child relationships.

---

### 6. Workflow Rules

Task status changes are governed by transition rules.

Current valid transitions are:

- `todo -> in_progress`
- `in_progress -> done`

Invalid transitions return `409 Conflict`.

The test suite verifies both valid and invalid transitions.

---

### 7. Data Integrity Rules

The application includes scoped uniqueness rules:

- project names must be unique per user
- task titles must be unique within a project

The test suite verifies both failing cases and allowed cases where the same names are used in different scopes.

This helps ensure that validation rules are not too weak or too broad.

---

### 8. Filtering and Pagination

The API supports filtering and pagination for selected resources.

Covered scenarios include:

- filtering by supported fields
- empty-result filtering cases
- first-page / second-page pagination behavior
- partial last page handling
- out-of-range or empty page behavior

This helps ensure that list endpoints remain predictable and consumer-friendly.

---

### 9. OpenAPI Contract Validation

The project includes OpenAPI contract tests against `/openapi.json`.

Current contract coverage includes:

- OpenAPI schema availability
- OpenAPI version/schema sanity checks
- core published API paths
- expected HTTP methods for core resources
- security metadata for protected endpoints

These tests help catch accidental contract regressions that could affect API consumers, generated docs, or future integrations.

---

## Test Design Approach

### Fixtures

Fixtures are used to provide:

- shared API client setup
- reusable database/session setup
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

Parametrized tests are used where multiple inputs should produce the same kind of result, such as invalid user name cases or other validation-focused scenarios.

This improves test clarity while reducing duplication.

---

## Test Isolation

The project now uses SQLite persistence instead of purely in-memory storage, so test isolation is handled through controlled setup/reset behavior in fixtures and helper utilities.

The test design aims to ensure:

- deterministic test outcomes
- minimal state leakage between tests
- reliable setup for resource creation and authorization scenarios

This is especially important for integration-style API testing.

---

## CI/CD Validation

The test suite is executed automatically in GitHub Actions on push and pull request events.

The CI pipeline currently performs the following:

- installs dependencies
- checks formatting with Black
- checks linting with Flake8
- runs the pytest suite
- checks code coverage
- enforces a minimum coverage threshold
- generates an HTML test report artifact

This ensures that quality checks are applied consistently outside the local environment.

---

## Out of Scope / Current Limitations

The current test strategy does not yet cover:

- load or performance testing
- browser/UI automation
- JWT-based authentication
- consumer-driven contract testing against an external service/specification
- Docker-based local execution validation on the current work machine

These remain possible future improvements.

---

## Future Enhancements

Potential next steps for expanding the testing strategy include:

- deeper OpenAPI response/schema validation
- broader security contract validation
- separate CI smoke and regression execution paths
- multi-version Python CI coverage
- improved test reporting/documentation
- Docker validation in an admin-enabled environment
- performance or reliability-focused testing where useful

---

## Summary

This testing strategy is designed to demonstrate practical QA automation skills beyond basic endpoint checks.

The suite validates:

- functionality
- validation behavior
- authentication and authorization boundaries
- workflow/state rules
- data integrity rules
- filtering and pagination behavior
- published OpenAPI contract stability

The project is structured to remain maintainable through fixtures, helpers, parametrized tests, CI quality gates, and supporting documentation.