from datetime import datetime
from typing import Optional
from fastapi import Depends
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
        print(f"Error executing query: {e}")
        users = []

    return users

def create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    hashed_password = user.password  # Aquí deberías aplicar un hash a la contraseña
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    
    return db_user

def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db_session)
):
    query = select(User).where(User.id == user_id)
    user = db.exec(query).first()

    if not user:
        return None

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        print(f"Error updating user: {e}")

    return user

def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    query = select(User).where(User.id == user_id)
    user = db.exec(query).first()

    if not user:
        return None
    
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {e}")

    return user