from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from crud.user import create_user, delete_user, read_users, update_user
from models.user import UserCreate, UserRead, UserUpdate
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
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")
    

@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db_session)):
    try:
        updated_user = update_user(user_id, user_update, db)

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {e}")
    
@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db_session)):
    try:
        deleted_user = delete_user(user_id, db)

        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting user: {e}")
