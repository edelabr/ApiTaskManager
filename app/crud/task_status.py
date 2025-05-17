from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from models.task_status import TaskStatus, TaskStatusCreate, TaskStatusUpdate
from db.database import get_db_session

def read_task_status(
    db: Session = Depends(get_db_session)
):
    query = select(TaskStatus)
    try:
        task_status = db.execute(query).scalars().all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting task status: {e}")

    if not task_status:
        raise HTTPException(status_code=404, detail="Task status not found")

    return task_status

def create_task_status(task_status: TaskStatusCreate, db: Session = Depends(get_db_session)):
    new_task_status = TaskStatus(
        name=task_status.name,
        color=task_status.color
    )
    try:
        db.add(new_task_status)
        db.commit()
        db.refresh(new_task_status)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating task status: {e}")
    
    return new_task_status

def update_task_status(
    id: int,
    task_status_update: TaskStatusUpdate,
    db: Session = Depends(get_db_session)
):
    query = select(TaskStatus).where(TaskStatus.id == id)
    task_status = db.exec(query).first()

    if not task_status:
        raise HTTPException(status_code=404, detail="Task status not found")

    for key, value in task_status_update.dict(exclude_unset=True).items():
        setattr(task_status, key, value)

    try:
        db.add(task_status)
        db.commit()
        db.refresh(task_status)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating task status: {e}")

    return task_status

def delete_task_status(id: int, db: Session = Depends(get_db_session)):
    query = select(TaskStatus).where(TaskStatus.id == id)
    task_status = db.exec(query).first()

    if not task_status:
        raise HTTPException(status_code=404, detail="Task status not found")
    
    try:
        db.delete(task_status)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting task status: {e}")

    return {"detail": "Task deleted successfully"}