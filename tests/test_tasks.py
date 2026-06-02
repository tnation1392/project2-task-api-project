import pytest, asyncio
from tests.helpers import create_user, build_auth_headers, create_project, create_task
from datetime import datetime


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_create_task(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Task Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Test Task"},
        headers=auth_headers
    )

    print("TASK STATUS:", task_res.status_code)
    print("TASK BODY:", task_res.text)

    assert task_res.status_code == 200

@pytest.mark.asyncio
async def test_get_tasks_for_project(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Task Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task 1"},
        headers=auth_headers
    )

    res = await client.get(f"/tasks/projects/{project_id}", headers=auth_headers)

    assert res.status_code == 200
    tasks = res.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"

@pytest.mark.asyncio
async def test_cannot_create_task_in_other_users_project(client):
    # User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # Create project with User A
    project_res = await client.post(
        "/projects/",
        json={"name": "Private"},
        headers=headers_a
    )
    project_id = project_res.json()["id"]

    # User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User B tries to create task
    res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Hack Task"},
        headers=headers_b
    )

    assert res.status_code == 403

@pytest.mark.asyncio
async def test_create_task_invalid_project(client, auth_headers):
    res = await client.post(
        "/tasks/projects/invalid-id",
        json={"title": "Test Task"},
        headers=auth_headers
    )

    assert res.status_code == 404

@pytest.mark.asyncio
async def test_update_task_status(client):
    user = await create_user(client, name="Task Owner")
    headers = build_auth_headers(user)

    project = await create_project(client, headers, name="Update Project")
    task = await create_task(client, headers, project["id"], title="Task")

    first_update = await client.patch(
        f"/tasks/{task['id']}",
        json={"status": "in_progress"},
        headers=headers
    )
    assert first_update.status_code == 200
    assert first_update.json()["status"] == "in_progress"

    second_update = await client.patch(
        f"/tasks/{task['id']}",
        json={"status": "done"},
        headers=headers
    )
    assert second_update.status_code == 200
    assert second_update.json()["status"] == "done"

@pytest.mark.asyncio
async def test_update_task_invalid_status(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Validation"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    res = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "invalid"},
        headers=auth_headers
    )

    assert res.status_code == 422

@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Delete Task"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    delete_res = await client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    # verify gone
    get_res = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers
    )
    assert get_res.status_code == 404

import pytest

@pytest.mark.asyncio
@pytest.mark.smoke
async def test_update_task_valid_transition_to_in_progress(client):
    user = await create_user(client, name="Task Owner")
    headers = build_auth_headers(user)

    project = await create_project(client, headers, name="Workflow Project")
    task = await create_task(client, headers, project["id"], title="Workflow Task")

    update_res = await client.patch(
        f"/tasks/{task['id']}",
        json={"status": "in_progress"},
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["status"] == "in_progress"


@pytest.mark.asyncio
@pytest.mark.regression
async def test_update_task_valid_transition_to_done(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Workflow Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Workflow Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    first_update = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "in_progress"},
        headers=auth_headers
    )
    assert first_update.status_code == 200

    second_update = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers
    )

    assert second_update.status_code == 200
    assert second_update.json()["status"] == "done"

@pytest.mark.asyncio
async def test_update_task_invalid_transition_todo_to_done(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Workflow Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Workflow Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    update_res = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers
    )

    assert update_res.status_code == 409
    assert "Invalid status transition" in update_res.json()["detail"]

@pytest.mark.asyncio
async def test_update_task_invalid_transition_done_to_todo(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Workflow Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Workflow Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    first_update = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "in_progress"},
        headers=auth_headers
    )
    assert first_update.status_code == 200

    second_update = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers
    )
    assert second_update.status_code == 200

    invalid_update = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "todo"},
        headers=auth_headers
    )

    assert invalid_update.status_code == 409
    assert "Invalid status transition" in invalid_update.json()["detail"]

@pytest.mark.asyncio
async def test_create_task_whitespace_only_title(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Validation Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    response = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "   "},
        headers=auth_headers
    )

    assert response.status_code == 422

@pytest.mark.asyncio
@pytest.mark.regression
async def test_cannot_create_duplicate_task_title_in_same_project(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Task Validation Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    first_response = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Duplicate Task"},
        headers=auth_headers
    )
    assert first_response.status_code == 200

    second_response = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Duplicate Task"},
        headers=auth_headers
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Task title already exists in this project"

@pytest.mark.asyncio
async def test_same_task_title_allowed_in_different_projects(client, auth_headers):
    project_res_1 = await client.post(
        "/projects/",
        json={"name": "Project One"},
        headers=auth_headers
    )
    project_id_1 = project_res_1.json()["id"]

    project_res_2 = await client.post(
        "/projects/",
        json={"name": "Project Two"},
        headers=auth_headers
    )
    project_id_2 = project_res_2.json()["id"]

    res1 = await client.post(
        f"/tasks/projects/{project_id_1}",
        json={"title": "Shared Task Name"},
        headers=auth_headers
    )
    res2 = await client.post(
        f"/tasks/projects/{project_id_2}",
        json={"title": "Shared Task Name"},
        headers=auth_headers
    )

    assert res1.status_code == 200
    assert res2.status_code == 200

@pytest.mark.asyncio
async def test_create_task_includes_timestamps(client):
    from tests.helpers import create_user, build_auth_headers, create_project

    user = await create_user(client, name="Timestamp User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Timestamp Project")

    response = await client.post(
        f"/tasks/projects/{project['id']}",
        json={"title": "Timestamp Task"},
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
async def test_update_task_changes_updated_at(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Audit User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Audit Project")
    task = await create_task(client, headers, project["id"], title="Audit Task")

    original_created_at = datetime.fromisoformat(task["created_at"])
    original_updated_at = datetime.fromisoformat(task["updated_at"])

    await asyncio.sleep(0.01)

    update_res = await client.patch(
        f"/tasks/{task['id']}",
        json={"status": "in_progress"},
        headers=headers
    )

    assert update_res.status_code == 200
    updated_task = update_res.json()

    new_created_at = datetime.fromisoformat(updated_task["created_at"])
    new_updated_at = datetime.fromisoformat(updated_task["updated_at"])

    assert new_created_at == original_created_at
    assert new_updated_at > original_updated_at

    @pytest.mark.asyncio
    async def test_get_tasks_filter_by_status(client):
        from tests.helpers import create_user, build_auth_headers, create_project, create_task

        user = await create_user(client, name="Filter User")
        headers = build_auth_headers(user)
        project = await create_project(client, headers, name="Filter Project")

        task1 = await create_task(client, headers, project["id"], title="Task One")
        task2 = await create_task(client, headers, project["id"], title="Task Two")

        await client.patch(
            f"/tasks/{task2['id']}",
            json={"status": "in_progress"},
            headers=headers
        )

        response = await client.get(
            f"/tasks/projects/{project['id']}?status=in_progress",
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["title"] == "Task Two"
        assert data[0]["status"] == "in_progress"

@pytest.mark.asyncio
async def test_get_tasks_filter_by_title_partial_match(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Search User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Search Project")

    await create_task(client, headers, project["id"], title="Fix login bug")
    await create_task(client, headers, project["id"], title="Write API tests")
    await create_task(client, headers, project["id"], title="Login validation review")

    response = await client.get(
        f"/tasks/projects/{project['id']}?title=login",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    returned_titles = [task["title"] for task in data]

    assert "Fix login bug" in returned_titles
    assert "Login validation review" in returned_titles

@pytest.mark.asyncio
async def test_get_tasks_filter_by_status_and_title(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Combined Filter User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Combined Filter Project")

    task1 = await create_task(client, headers, project["id"], title="Bug review")
    task2 = await create_task(client, headers, project["id"], title="Bug fix")
    await create_task(client, headers, project["id"], title="Documentation update")

    await client.patch(
        f"/tasks/{task1['id']}",
        json={"status": "in_progress"},
        headers=headers
    )

    await client.patch(
        f"/tasks/{task2['id']}",
        json={"status": "in_progress"},
        headers=headers
    )

    response = await client.get(
        f"/tasks/projects/{project['id']}?status=in_progress&title=fix",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Bug fix"
    assert data[0]["status"] == "in_progress"

@pytest.mark.asyncio
async def test_get_tasks_filter_returns_empty_list_when_no_match(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Empty Filter User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Empty Filter Project")

    await create_task(client, headers, project["id"], title="Alpha task")
    await create_task(client, headers, project["id"], title="Beta task")

    response = await client.get(
        f"/tasks/projects/{project['id']}?title=gamma",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_tasks_pagination_first_page(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Pagination User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Pagination Project")

    for i in range(5):
        await create_task(client, headers, project["id"], title=f"Task {i + 1}")

    response = await client.get(
        f"/tasks/projects/{project['id']}?page=1&size=2",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2

@pytest.mark.asyncio
async def test_get_tasks_pagination_second_page(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Pagination User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Pagination Project")

    for i in range(5):
        await create_task(client, headers, project["id"], title=f"Task {i + 1}")

    response_page_1 = await client.get(
        f"/tasks/projects/{project['id']}?page=1&size=2",
        headers=headers
    )
    response_page_2 = await client.get(
        f"/tasks/projects/{project['id']}?page=2&size=2",
        headers=headers
    )

    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200

    page_1_ids = [task["id"] for task in response_page_1.json()]
    page_2_ids = [task["id"] for task in response_page_2.json()]

    assert len(page_1_ids) == 2
    assert len(page_2_ids) == 2
    assert set(page_1_ids).isdisjoint(set(page_2_ids))


@pytest.mark.asyncio
async def test_get_tasks_pagination_last_partial_page(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Partial Page User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Partial Page Project")

    for i in range(5):
        await create_task(client, headers, project["id"], title=f"Task {i + 1}")

    response = await client.get(
        f"/tasks/projects/{project['id']}?page=3&size=2",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1

@pytest.mark.asyncio
async def test_get_tasks_pagination_empty_page(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Empty Page User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Empty Page Project")

    for i in range(3):
        await create_task(client, headers, project["id"], title=f"Task {i + 1}")

    response = await client.get(
        f"/tasks/projects/{project['id']}?page=5&size=2",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_tasks_pagination_invalid_page(client):
    from tests.helpers import create_user, build_auth_headers, create_project

    user = await create_user(client, name="Invalid Page User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Invalid Page Project")

    response = await client.get(
        f"/tasks/projects/{project['id']}?page=0&size=2",
        headers=headers
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_tasks_pagination_invalid_size(client):
    from tests.helpers import create_user, build_auth_headers, create_project

    user = await create_user(client, name="Invalid Size User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Invalid Size Project")

    response = await client.get(
        f"/tasks/projects/{project['id']}?page=1&size=0",
        headers=headers
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_tasks_filtering_and_pagination_together(client):
    from tests.helpers import create_user, build_auth_headers, create_project, create_task

    user = await create_user(client, name="Filter Page User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Filter Page Project")

    tasks = []
    for i in range(5):
        task = await create_task(client, headers, project["id"], title=f"Bug Task {i + 1}")
        tasks.append(task)

    for task in tasks[:4]:
        await client.patch(
            f"/tasks/{task['id']}",
            json={"status": "in_progress"},
            headers=headers
        )

    response = await client.get(
        f"/tasks/projects/{project['id']}?status=in_progress&page=2&size=2",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert all(task["status"] == "in_progress" for task in data)

