from sqlalchemy.orm import Session

from todo_api.models import TodoItem
from todo_api.schemas import TodoCreate, TodoUpdate


def create_todo(db: Session, data: TodoCreate) -> TodoItem:
    todo = TodoItem(title=data.title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session) -> list[TodoItem]:
    return db.query(TodoItem).all()


def get_todo(db: Session, todo_id: int) -> TodoItem | None:
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()


def update_todo(db: Session, todo_id: int, data: TodoUpdate) -> TodoItem | None:
    todo = get_todo(db, todo_id)
    if todo is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int) -> bool:
    todo = get_todo(db, todo_id)
    if todo is None:
        return False
    db.delete(todo)
    db.commit()
    return True
