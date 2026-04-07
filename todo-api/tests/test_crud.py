import pytest

from todo_api.crud import create_todo, get_todos, get_todo, update_todo, delete_todo
from todo_api.schemas import TodoCreate, TodoUpdate


def test_create_todo(db_session):
    todo = create_todo(db_session, TodoCreate(title="Test item"))
    assert todo.id is not None
    assert todo.title == "Test item"
    assert todo.completed is False
    assert todo.description is None


def test_create_todo_with_description(db_session):
    todo = create_todo(db_session, TodoCreate(title="Test", description="Some details"))
    assert todo.description == "Some details"


def test_get_todos(db_session):
    create_todo(db_session, TodoCreate(title="Item 1"))
    create_todo(db_session, TodoCreate(title="Item 2"))
    todos = get_todos(db_session)
    assert len(todos) == 2


def test_get_todo(db_session):
    todo = create_todo(db_session, TodoCreate(title="Find me"))
    found = get_todo(db_session, todo.id)
    assert found is not None
    assert found.title == "Find me"


def test_get_todo_not_found(db_session):
    found = get_todo(db_session, 999)
    assert found is None


def test_update_todo(db_session):
    todo = create_todo(db_session, TodoCreate(title="Old title"))
    updated = update_todo(db_session, todo.id, TodoUpdate(title="New title", completed=True))
    assert updated is not None
    assert updated.title == "New title"
    assert updated.completed is True


def test_update_todo_not_found(db_session):
    result = update_todo(db_session, 999, TodoUpdate(title="Nope"))
    assert result is None


def test_delete_todo(db_session):
    todo = create_todo(db_session, TodoCreate(title="Delete me"))
    assert delete_todo(db_session, todo.id) is True
    assert get_todo(db_session, todo.id) is None


def test_delete_todo_not_found(db_session):
    assert delete_todo(db_session, 999) is False
