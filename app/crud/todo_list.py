from typing import Optional
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_db_session
from app.models.todo_list import TodoList, TodoListCreate, TodoListRead, TodoListUpdate
from app.models.user import User

def read_todo_list(
    id: Optional[int] = None,
    owner_id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends()
):
    query = select(TodoList.id, TodoList.title, TodoList.description, User.username, TodoList.created_at).join(User, TodoList.owner_id == User.id)

    if current_user["role"] in ["user"]:
        query = query.where(User.username == current_user["sub"])
    if id:
        query = query.where(TodoList.id == id)
    if owner_id:
        query = query.where(TodoList.owner_id == owner_id)
    if username:
        query = query.where(User.username == username)
    if email:
        query = query.where(User.email == email)

    query = query.offset(skip).limit(limit)
    
    try:
        todo_lists = db.execute(query).fetchall()
    
        new_todo_lists = []
        for todo_list in todo_lists:
            todo_list_read = TodoListRead(
                id=todo_list[0],
                title=todo_list[1],
                description=todo_list[2],
                owner_username=todo_list[3],
                created_at=todo_list[4]
            )
            new_todo_lists.append(todo_list_read)
    except Exception as e:
        raise Exception(e)
    
    if not todo_lists:
        raise HTTPException(status_code=404, detail="Todo lists not found")

    return new_todo_lists

def create_todo_list(
    todo_list_create: TodoListCreate, 
    db: Session = Depends(get_db_session), 
    current_user: dict = Depends()
):
    # Validar que el owner_username existe en la base de datos de usuarios
    owner_query = select(User).where(User.username == todo_list_create.owner_username)
    owner = db.exec(owner_query).first()

    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    if current_user["role"] in ["user"] and current_user["sub"] != owner.username:
        raise HTTPException(status_code=403, detail="Insufficient permissions to create todo list to other users")
    
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
        raise Exception(e)

    return returned_new_list 

def update_todo_list(
    id: int,
    todo_list_update: TodoListUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends()
):
    query = select(TodoList).where(TodoList.id == id)
    todo_list = db.exec(query).first()

    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")

    for key, value in todo_list_update.dict(exclude_unset=True).items():
        setattr(todo_list, key, value)

    owner_query = select(User).where(User.id == todo_list.owner_id)
    owner = db.exec(owner_query).first()

    if current_user["role"] in ["user"] and current_user["sub"] != owner.username:
        raise HTTPException(status_code=403, detail="Insufficient permissions to update todo list to other users")

    try:
        db.add(todo_list)
        db.commit()
        db.refresh(todo_list)

        returned_new_list = TodoListRead(
        id=todo_list.id,
        title=todo_list.title,
        description=todo_list.description,
        owner_username=owner.username,
        created_at=todo_list.created_at
    )
    except Exception as e:
        db.rollback()
        raise Exception(e)

    return returned_new_list

def delete_todo_list(
    id: int, 
    db: Session = Depends(get_db_session), 
    current_user: dict = Depends()
):
    query = select(TodoList).where(TodoList.id == id)
    todo_list = db.exec(query).first()

    owner_query = select(User).where(User.id == todo_list.owner_id)
    owner = db.exec(owner_query).first()

    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    if current_user["role"] in ["user"] and current_user["sub"] != owner.username:
        raise HTTPException(status_code=403, detail="Insufficient permissions to update todo list to other users")
    
    try:
        db.delete(todo_list)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(e)

    return {"detail": "Todo list deleted successfully"}
