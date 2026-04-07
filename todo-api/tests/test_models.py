# todo-api/tests/test_models.py
from todo_api.models import TodoItem


def test_todo_item_creation(db_session):
    todo = TodoItem(title="Buy milk")
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    assert todo.id is not None
    assert todo.title == "Buy milk"
    assert todo.completed is False
    assert todo.created_at is not None
