def test_create_todo(client):
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_todo_empty_title(client):
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


def test_get_todos(client):
    client.post("/todos", json={"title": "Item 1"})
    client.post("/todos", json={"title": "Item 2"})
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_todo(client):
    create_resp = client.post("/todos", json={"title": "Old"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "New", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New"
    assert data["completed"] is True


def test_update_todo_not_found(client):
    response = client.put("/todos/999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_todo(client):
    create_resp = client.post("/todos", json={"title": "Delete me"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204

    get_resp = client.get("/todos")
    assert len(get_resp.json()) == 0


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
