from asyncio import Task
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .user import User

class TodoList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional[User] = Relationship(back_populates="todo_list")
    tasks: List["Task"] = Relationship(back_populates="todo_list")