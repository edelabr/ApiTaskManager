from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class TaskStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    color: Optional[str] = None
