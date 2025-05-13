from datetime import datetime
from typing import Optional
from fastapi import Depends
from sqlmodel import Session

from models.user import User, UserCreate
from db.database import get_db_session

def read_users(
    id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    try:
        query = db.query(User)

        if id:
            query = query.filter(User.id == id)
        if username:
            query = query.filter(User.username == username)
        if email:
            query = query.filter(User.email == email)

        users = query.offset(skip).limit(limit).all()
    except Exception as e:
        print(f"Error getting user: {e}")
        
    return users

def create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    hashed_password = user.password  # Aquí deberías aplicar un hash a la contraseña
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    
    return db_user