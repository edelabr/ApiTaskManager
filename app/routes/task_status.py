from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from crud.task_status import create_task_status, delete_task_status, read_task_status, update_task_status
from models.task_status import TaskStatusCreate, TaskStatusRead, TaskStatusUpdate
from db.database import get_db_session

router = APIRouter(prefix="/task_status", tags=["task_status"])

@router.get("/", response_model=List[TaskStatusRead])
def get_task_status_endpoint(
    db: Session = Depends(get_db_session)
):
    return read_task_status(db)

@router.post("/", response_model=TaskStatusRead, status_code=201)
def add_task_status_endpoint(task_status: TaskStatusCreate, db: Session = Depends(get_db_session)):
    return create_task_status(task_status, db)
        
@router.put("/{id}", response_model=TaskStatusRead)
def update_task_status_endpoint(id: int, task_status_update: TaskStatusUpdate, db: Session = Depends(get_db_session)):
    return update_task_status(id, task_status_update, db)
    
@router.delete("/{id}", status_code=204)
def delete_task_status_endpoint(id: int, db: Session = Depends(get_db_session)):
    return delete_task_status(id, db)
