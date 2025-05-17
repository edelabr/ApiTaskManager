from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class TodoList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoListCreate(SQLModel):
    title: str
    description: str
    owner_username: str

class TodoListRead(SQLModel):
    id: int
    title: str
    description: str
    owner_username: str
    created_at: datetime

class TodoListUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None