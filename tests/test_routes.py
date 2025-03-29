import pytest
from fastapi.testclient import TestClient
import os
import sqlite3

# Remove the test database if it exists
def setup_module(module):
    if os.path.exists("todo.db"):
        os.remove("todo.db")

    # Initialize the database for testing
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()


# Import the app after deleting and recreating the database
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running"}


def test_create_todo():
    response = client.post(
        "/api/todos",
        json={"title": "Test todo", "description": "Test description", "completed": False},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["completed"] == False
    assert "id" in data
    todo_id = data["id"]

    # Check that the todo has been successfully created
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == data


def test_get_todos():
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Check that there is at least one todo (the one created earlier)
    assert len(response.json()) > 0


def test_update_todo():
    # Create a todo for testing
    response = client.post(
        "/api/todos",
        json={"title": "Update Test", "description": "Will be updated", "completed": False},
    )
    todo_id = response.json()["id"]

    # Update the todo
    response = client.put(
        f"/api/todos/{todo_id}",
        json={"title": "Updated", "description": "Has been updated", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["description"] == "Has been updated"
    assert data["completed"] == True


def test_delete_todo():
    # Create a todo for testing
    response = client.post(
        "/api/todos",
        json={"title": "Delete Test", "description": "Will be deleted", "completed": False},
    )
    todo_id = response.json()["id"]

    # Delete the todo
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 204

    # Check that the todo has been deleted
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 404
