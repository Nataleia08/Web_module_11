from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config():
