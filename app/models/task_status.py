from typing import Optional
from sqlmodel import SQLModel, Field

class TaskStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    color: Optional[str] = None

class TaskStatusCreate(SQLModel):
    name: str
    color: str

class TaskStatusRead(SQLModel):
    id: int
    name: str
    color: str

class TaskStatusUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
