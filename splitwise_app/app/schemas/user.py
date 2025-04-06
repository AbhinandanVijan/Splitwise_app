from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared base schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Schema for user creation (password input)
class UserCreate(UserBase):
    password: str

# Schema for response/output
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
