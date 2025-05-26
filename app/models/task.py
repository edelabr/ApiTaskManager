from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool = Field(default=False)
    todo_list_id: int   = Field(foreign_key="todolist.id")
    status_id:    int   = Field(foreign_key="taskstatus.id")

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at:   datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    is_completed: bool

class TaskRead(TaskBase):
    id: int
    created_at:   datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    status_id:    Optional[int] = None
