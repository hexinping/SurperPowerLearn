from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from todo_api.crud import create_todo, delete_todo, get_todo, get_todos, update_todo
from todo_api.database import Base, engine, get_db
from todo_api.schemas import TodoCreate, TodoResponse, TodoUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create(data: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db, data)


@app.get("/todos", response_model=list[TodoResponse])
def read_all(db: Session = Depends(get_db)):
    return get_todos(db)


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    todo = update_todo(db, todo_id, data)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete(todo_id: int, db: Session = Depends(get_db)):
    if not delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=204)
