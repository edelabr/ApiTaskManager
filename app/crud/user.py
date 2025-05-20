from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from models.user import User, UserCreate, UserUpdate
from db.database import get_db_session

def read_users(
    id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    query = select(User)

    if id:
        query = query.where(User.id == id)
    if username:
        query = query.where(User.username == username)
    if email:
        query = query.where(User.email == email)

    query = query.offset(skip).limit(limit)
    
    try:
        users = db.execute(query).scalars().all()
    except Exception as e:
        raise Exception(e)

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    return users

def create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    hashed_password = user.password  # Aquí deberías aplicar un hash a la contraseña
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise Exception(e)
    
    return new_user

def update_user(
    id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db_session)
):
    query = select(User).where(User.id == id)
    user = db.exec(query).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise Exception(e)

    return user

def delete_user(id: int, db: Session = Depends(get_db_session)):
    query = select(User).where(User.id == id)
    user = db.exec(query).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(e)

    return {"detail": "User deleted successfully"}