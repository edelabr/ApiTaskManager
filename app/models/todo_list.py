from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class TodoListBase(SQLModel):
    title: str
    description: Optional[str] = None

class TodoList(TodoListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoListCreate(TodoListBase):
    owner_username: str

class TodoListRead(TodoListBase):
    id: int
    owner_username: str
    created_at: datetime

class TodoListUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None