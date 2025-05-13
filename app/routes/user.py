from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from crud.user import create_user, read_users
from models.user import UserCreate, UserRead
from db.database import get_db_session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def get_users(
    id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    users = read_users(id, username, email, skip, limit, db)
    
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    
    return users

@router.post("/", response_model=UserRead, status_code=201)
def add_user(user: UserCreate, db: Session = Depends(get_db_session)):
    try:
        return create_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating TaskStatus: {e}")
