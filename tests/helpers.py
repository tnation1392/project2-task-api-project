async def create_user(client, name="Test User", role="member"):
    response = await client.post("/users/", json={"name": name, "role": role})
    assert response.status_code == 200
    return response.json()


def build_auth_headers(user_data):
    return {"x-api-key": user_data["api_key"]}


async def create_project(client, headers, name="Test Project"):
    response = await client.post(
        "/projects/",
        json={"name": name},
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


async def create_task(client, headers, project_id, title="Test Task"):
    response = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": title},
        headers=headers
    )
    assert response.status_code == 200
    return response.json()