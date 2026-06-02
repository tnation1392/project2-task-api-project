import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_openapi_schema_contains_expected_methods():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    paths = schema["paths"]

    # Projects
    assert {"get", "post"} <= set(paths["/projects/"].keys())
    assert {"get", "delete"} <= set(paths["/projects/{project_id}"].keys())

    # Tasks
    assert {"get", "post"} <= set(paths["/tasks/projects/{project_id}"].keys())
    assert {"patch", "delete"} <= set(paths["/tasks/{task_id}"].keys())


@pytest.mark.asyncio
async def test_openapi_schema_includes_api_key_security_metadata():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()

    components = schema.get("components", {})
    security_schemes = components.get("securitySchemes", {})

    assert security_schemes, "No OpenAPI securitySchemes found"

    api_key_schemes = [
        scheme
        for scheme in security_schemes.values()
        if scheme.get("type") == "apiKey" and scheme.get("in") == "header"
    ]

    assert api_key_schemes, (
        f"No header-based apiKey security scheme found. "
        f"Actual securitySchemes: {security_schemes}"
    )

    paths = schema["paths"]

    protected_paths = [
        "/projects/",
        "/projects/{project_id}",
        "/tasks/projects/{project_id}",
        "/tasks/{task_id}",
    ]

    for path in protected_paths:
        operation_security_found = any(
            "security" in operation and operation["security"]
            for operation in paths[path].values()
            if isinstance(operation, dict)
        )
        assert operation_security_found, (
            f"No OpenAPI security metadata found for protected path: {path}"
        )
    print(paths["/projects/"])