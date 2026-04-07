from datetime import datetime

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}
