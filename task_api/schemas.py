from typing import Optional
from pydantic import BaseModel, Field
from pydantic import EmailStr


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["abc","a_b_c"])

    email: EmailStr = Field(..., examples=["abcd@example.com"])

    password: str = Field(..., min_length=6, max_length=30, examples=["secretpass123"])


class UserOut(BaseModel):

    id: int

    username: str

    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str 
    token_type: str="bearer"

class TaskCreate(BaseModel):

    title: str = Field(..., min_length=1, max_length=100, examples=["Study Fastapi"])

    description: Optional[str] = Field(None,examples=["Learn Fastapi from Scratch"])

    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high|critical)$",
        examples=["high"],
    )

class TaskUpdate(BaseModel):

    title: Optional[str] = Field(None, min_length=1, max_length=100)

    description: Optional[str] = None

    priority: Optional[str] = Field(None,pattern="^(low|medium|high|critical)$")

    is_completed: Optional[bool] = None



class TaskOut(BaseModel):

    id: int

    title:str

    description: Optional[str]

    priority: str

    is_completed: bool

    owner_id: int

    class Config:
        from_attributes = True