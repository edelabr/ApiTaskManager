from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_db_session
from models.todo_list import TodoList, TodoListCreate, TodoListRead
from models.user import User


def create_todo_list(todo_list_create: TodoListCreate, db: Session = Depends(get_db_session)):
    # Validar que el owner_username existe en la base de datos de usuarios
    owner_query = select(User).where(User.username == todo_list_create.owner_username)
    owner = db.exec(owner_query).first()

    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    try:
        new_todo_list = TodoList(
        title=todo_list_create.title,
        description=todo_list_create.description,
        owner_id=owner.id
        )
        db.add(new_todo_list)
        db.commit()
        db.refresh(new_todo_list)

        returned_new_list = TodoListRead(
        id=new_todo_list.id,
        title=new_todo_list.title,
        description=new_todo_list.description,
        owner_username=owner.username,
        created_at=new_todo_list.created_at
    )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating todo_list: {e}")

    return returned_new_list 