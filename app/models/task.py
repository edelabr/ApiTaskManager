from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .todo_list import TodoList
from .task_status import TaskStatus

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool = False
    todo_list_id: int = Field(foreign_key="todolist.id")
    status_id: int = Field(foreign_key="taskstatus.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    todo_list: Optional[TodoList] = Relationship(back_populates="task")
    status: Optional[TaskStatus] = Relationship(back_populates="task")