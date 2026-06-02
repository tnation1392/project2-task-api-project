import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_openapi_schema_contains_core_resource_paths():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()

    assert "openapi" in schema
    assert schema["openapi"].startswith("3.")
    assert "paths" in schema

    actual_paths = set(schema["paths"].keys())

    expected_exact_paths = {
        "/",
        "/projects/",
        "/projects/{project_id}",
        "/tasks/projects/{project_id}",
        "/tasks/{task_id}",
        "/users/{user_id}",
    }

    missing_exact_paths = expected_exact_paths - actual_paths
    assert (
        not missing_exact_paths
    ), f"Missing exact OpenAPI paths: {sorted(missing_exact_paths)}"

    assert any(
        path.rstrip("/") == "/users" for path in actual_paths
    ), f"Users collection path not found. Actual OpenAPI paths: {sorted(actual_paths)}"
