from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.dependencies import require_role
from app.crud.task import create_task, delete_task, read_tasks, update_task
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.db.database import get_db_session

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
def get_tasks_endpoint(
    id: Optional[int] = None,
    is_completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session), 
    current_user: dict = Depends(require_role("admin", "user", "viewer"))
):
    return read_tasks(id, is_completed, skip, limit, db, current_user)

@router.post("/", response_model=TaskRead, status_code=201)
def add_task_endpoint(task: TaskCreate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))):
    return create_task(task, db, current_user)
        
@router.put("/{id}", response_model=TaskRead)
def update_task_endpoint(id: int, task_update: TaskUpdate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))):
    return update_task(id, task_update, db, current_user)
    
@router.delete("/{id}")
def delete_task_endpoint(id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))):
    return delete_task(id, db, current_user)
