import pytest
from tests.helpers import create_user, build_auth_headers, create_project
from datetime import datetime

@pytest.mark.asyncio
@pytest.mark.smoke
async def test_create_project(client, auth_headers):
    response = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Project"
    assert "id" in data
    assert "owner_id" in data

@pytest.mark.asyncio
@pytest.mark.smoke
async def test_get_projects_returns_only_user_projects(client, auth_user, auth_headers):
    # Create project for this user
    await client.post("/projects/", json={"name": "Project A"}, headers=auth_headers)

    response = await client.get("/projects/", headers=auth_headers)

    assert response.status_code == 200

    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["name"] == "Project A"

@pytest.mark.asyncio
async def test_users_cannot_see_each_others_projects(client):
    # User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User A creates project
    await client.post("/projects/", json={"name": "A Project"}, headers=headers_a)

    # User B fetches projects
    res = await client.get("/projects/", headers=headers_b)

    assert res.status_code == 200
    assert res.json() == []  # Should NOT see User A's project

@pytest.mark.asyncio
@pytest.mark.regression
async def test_cannot_access_other_users_project(client):
    # Create User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # Create project with User A
    project_res = await client.post(
        "/projects/",
        json={"name": "Private Project"},
        headers=headers_a
    )
    project_id = project_res.json()["id"]

    # Create User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User B tries to access User A's project
    res = await client.get(f"/projects/{project_id}", headers=headers_b)

    assert res.status_code == 403

@pytest.mark.asyncio
async def test_get_nonexistent_project(client, auth_headers):
    res = await client.get("/projects/nonexistent-id", headers=auth_headers)

    assert res.status_code == 404

@pytest.mark.asyncio
@pytest.mark.regression
async def test_delete_project(client):
    user = await create_user(client, name="Project Owner")
    headers = build_auth_headers(user)

    project = await create_project(client, headers, name="Delete Me")
    project_id = project["id"]

    delete_res = await client.delete(f"/projects/{project_id}", headers=headers)
    assert delete_res.status_code == 200

    get_res = await client.get(f"/projects/{project_id}", headers=headers)
    assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_projects_require_auth(client):
    res = await client.get("/projects/")

    assert res.status_code == 401

@pytest.mark.asyncio
@pytest.mark.regression
async def test_cannot_create_duplicate_project_name_for_same_user(client, auth_headers):
    first_response = await client.post(
        "/projects/",
        json={"name": "Duplicate Project"},
        headers=auth_headers
    )
    assert first_response.status_code == 200

    second_response = await client.post(
        "/projects/",
        json={"name": "Duplicate Project"},
        headers=auth_headers
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Project name already exists for this user"

@pytest.mark.asyncio
async def test_create_project_whitespace_only_name(client, auth_headers):
    response = await client.post(
        "/projects/",
        json={"name": "   "},
        headers=auth_headers
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_different_users_can_create_same_project_name(client):
    # User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # Both create a project with the same name
    res1 = await client.post(
        "/projects/",
        json={"name": "Shared Name"},
        headers=headers_a
    )
    res2 = await client.post(
        "/projects/",
        json={"name": "Shared Name"},
        headers=headers_b
    )

    assert res1.status_code == 200
    assert res2.status_code == 200

@pytest.mark.asyncio
async def test_different_users_can_create_same_project_name(client):
    # Create User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # Create User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User A creates a project
    res1 = await client.post(
        "/projects/",
        json={"name": "Shared Name"},
        headers=headers_a
    )

    # User B creates a project with the same name
    res2 = await client.post(
        "/projects/",
        json={"name": "Shared Name"},
        headers=headers_b
    )

    assert res1.status_code == 200
    assert res2.status_code == 200

@pytest.mark.asyncio
async def test_create_project_includes_timestamps(client):
    from tests.helpers import create_user, build_auth_headers

    user = await create_user(client, name="Timestamp User")
    headers = build_auth_headers(user)

    response = await client.post(
        "/projects/",
        json={"name": "Timestamp Project"},
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "created_at" in data
    assert "updated_at" in data

    created_at = datetime.fromisoformat(data["created_at"])
    updated_at = datetime.fromisoformat(data["updated_at"])

    assert created_at <= updated_at

@pytest.mark.asyncio
async def test_admin_can_view_other_users_project(client):
    from tests.helpers import create_user, build_auth_headers, create_project

    member = await create_user(client, name="Member User")
    member_headers = build_auth_headers(member)
    project = await create_project(client, member_headers, name="Member Project")

    admin_response = await client.post("/users/", json={"name": "Admin User", "role": "admin"})
    admin = admin_response.json()
    admin_headers = {"x-api-key": admin["api_key"]}

    response = await client.get(f"/projects/{project['id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["id"] == project["id"]

@pytest.mark.asyncio
async def test_admin_can_see_all_projects(client):
    from tests.helpers import create_user, build_auth_headers, create_project

    member1 = await create_user(client, name="Member One")
    headers1 = build_auth_headers(member1)
    await create_project(client, headers1, name="Project One")

    member2 = await create_user(client, name="Member Two")
    headers2 = build_auth_headers(member2)
    await create_project(client, headers2, name="Project Two")

    admin_response = await client.post("/users/", json={"name": "Admin User", "role": "admin"})
    admin = admin_response.json()
    admin_headers = {"x-api-key": admin["api_key"]}

    response = await client.get("/projects/", headers=admin_headers)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
