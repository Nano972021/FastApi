from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Create post request validation model
class PostCreate(PostBase):
    pass

# Get Post response validation model
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# Create User request validation model
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Get User response validation model
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

# Login request validation model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token Validation Model
class Token(BaseModel):
    access_token: str
    type: str

# Token Data validation model
class TokenData(BaseModel):
    id : Optional[str]

