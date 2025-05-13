from datetime import datetime
from typing import Optional, List
from app.models.todo_list import TodoList
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.timezone.utc)

    todo_lists: List["TodoList"] = Relationship(back_populates="owner")