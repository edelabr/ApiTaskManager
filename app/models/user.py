from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
from pydantic import EmailStr

class RoleEnum(str, Enum):
    user = 'user'
    viewer = 'viewer'

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    role: str = Field(default="user")  # Default role is "user"

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    refresh_token: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user

class UserRead(UserBase):
    id: int
    created_at: datetime

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
