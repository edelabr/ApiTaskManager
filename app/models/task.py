from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool = Field(default=False)
    todo_list_id: int   = Field(foreign_key="todolist.id")
    status_id:    int   = Field(foreign_key="taskstatus.id")
    created_at:   datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(SQLModel):
    title: str
    description:str
    due_date: date
    is_completed: bool
    todo_list_id: int   = Field(foreign_key="todolist.id")
    status_id:    int   = Field(foreign_key="taskstatus.id")

class TaskRead(SQLModel):
    id: int
    title: str
    description:str
    due_date: date
    is_completed: bool
    todo_list_id: int 
    status_id:    int
    created_at:   datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    status_id:    Optional[int] = None
