from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from crud.todo_list import create_todo_list, read_todo_list
from db.database import get_db_session
from models.todo_list import TodoListCreate, TodoListRead


router = APIRouter(prefix="/todo_lists", tags=["todo_lists"])

@router.get("/", response_model=List[TodoListRead])
def get_todo_list(
    id: Optional[int] = None,
    owner_id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    return read_todo_list(id, owner_id, username, email, skip, limit, db)

@router.post("/", response_model=TodoListRead, status_code=201)
def add_todo_list(todo_list: TodoListCreate, db: Session = Depends(get_db_session)):
    return create_todo_list(todo_list, db)