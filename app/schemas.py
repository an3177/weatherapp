from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserSignup(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class UserOut(BaseModel):
    email:EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


