from typing import Optional
from sqlmodel import SQLModel, Field

class TaskStatusBase(SQLModel):
    name: str
    color: Optional[str] = None

class TaskStatus(TaskStatusBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TaskStatusCreate(TaskStatusBase):
    color: str

class TaskStatusRead(TaskStatusBase):
    id: int

class TaskStatusUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
