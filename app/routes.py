from fastapi import APIRouter, HTTPException
import sqlite3
from typing import List

from app.models import Todo, TodoCreate

router = APIRouter()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@router.get("/todos", response_model=List[Todo])
async def get_todos():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return todos


@router.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (todo.title, todo.description, todo.completed)
    )
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {**todo.dict(), "id": todo_id}


@router.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    conn = sqlite3.connect('todo.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    conn.close()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoCreate):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (todo.title, todo.description, todo.completed, todo_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    conn.commit()
    conn.close()

    return {**todo.dict(), "id": todo_id}


@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    conn.commit()
    conn.close()

    return None