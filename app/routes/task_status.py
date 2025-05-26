from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.dependencies import require_role
from app.crud.task_status import create_task_status, delete_task_status, read_task_status, update_task_status
from app.models.task_status import TaskStatusCreate, TaskStatusRead, TaskStatusUpdate
from app.db.database import get_db_session

router = APIRouter(prefix="/task_status", tags=["task_status"])

@router.get("/", response_model=List[TaskStatusRead])
def get_task_status_endpoint(
    db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user"))
):
    return read_task_status(db, current_user)

@router.post("/", response_model=TaskStatusRead, status_code=201)
def add_task_status_endpoint(task_status: TaskStatusCreate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin"))):
    return create_task_status(task_status, db, current_user)
        
@router.put("/{id}", response_model=TaskStatusRead)
def update_task_status_endpoint(id: int, task_status_update: TaskStatusUpdate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin"))):
    return update_task_status(id, task_status_update, db, current_user)
    
@router.delete("/{id}")
def delete_task_status_endpoint(id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin"))):
    return delete_task_status(id, db, current_user)
