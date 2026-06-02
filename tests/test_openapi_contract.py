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
