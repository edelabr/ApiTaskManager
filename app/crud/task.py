
from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from db.database import get_db_session
from models.task import Task, TaskCreate, TaskUpdate


def read_tasks(
    id: Optional[int] = None,
    is_completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    query = select(Task)

    if id:
        query = query.where(Task.todo_list_id == id)
    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)

    query = query.offset(skip).limit(limit)
    
    try:
        tasks = db.execute(query).scalars().all()
    except Exception as e:
        raise Exception(e)

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    return tasks

def create_task(task: TaskCreate, db: Session = Depends(get_db_session)):
    try:
        new_task = Task(
        title = task.title,
        description = task.description,
        due_date = task.due_date,
        is_completed = task.is_completed,
        todo_list_id = task.todo_list_id,
        status_id = task.status_id,
        created_at = datetime.utcnow()
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception as e:
        db.rollback()
        raise Exception(e)
    
    return new_task

def update_task(
    id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db_session)
):
    query = select(Task).where(Task.id == id)
    task = db.exec(query).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception as e:
        db.rollback()
        raise Exception(e)

    return task

def delete_task(id: int, db: Session = Depends(get_db_session)):
    query = select(Task).where(Task.id == id)
    task = db.exec(query).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        db.delete(task)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(e)

    return {"detail": "Task deleted successfully"}