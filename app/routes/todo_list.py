from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.dependencies import require_role
from app.crud.todo_list import create_todo_list, read_todo_list, update_todo_list, delete_todo_list
from app.db.database import get_db_session
from app.models.todo_list import TodoListCreate, TodoListRead, TodoListUpdate


router = APIRouter(prefix="/todo_lists", tags=["todo_lists"])

@router.get("/", response_model=List[TodoListRead])
def get_todo_list_endpoint(
    id: Optional[int] = None,
    owner_id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(require_role("admin", "user", "viewer"))
):
    return read_todo_list(id, owner_id, username, email, skip, limit, db, current_user)

@router.post("/", response_model=TodoListRead, status_code=201)
def add_todo_list_endpoint(todo_list: TodoListCreate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))):
    return create_todo_list(todo_list, db, current_user)

@router.put("/{id}", response_model=TodoListRead)
def update_todo_list_endpoint(id: int, todo_list_update: TodoListUpdate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))):
    return update_todo_list(id, todo_list_update, db, current_user)

@router.delete("/{id}")
def delete_todo_list_endpoint(id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))):
    return delete_todo_list(id, db, current_user)