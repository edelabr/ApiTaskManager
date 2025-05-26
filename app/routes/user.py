from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from auth.dependencies import require_role
from crud.user import create_user, delete_user, read_users, update_user
from models.user import UserCreate, UserRead, UserUpdate
from db.database import get_db_session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def get_users_endpoint(
    id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(require_role("admin", "user", "viewer"))
):
    return read_users(id, username, email, skip, limit, db, current_user)

@router.post("/", response_model=UserRead, status_code=201)
def add_user_endpoint(user: UserCreate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin"))):
    return create_user(user, db, current_user)
        
@router.put("/{id}", response_model=UserRead)
def update_user_endpoint(id: int, user_update: UserUpdate, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user", "viewer"))):
    return update_user(id, user_update, db, current_user)
    
@router.delete("/{id}", status_code=204)
def delete_user_endpoint(id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(require_role("admin", "user", "viewer"))):
    return delete_user(id, db, current_user)
