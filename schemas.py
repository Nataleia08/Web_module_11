from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    firs_name: str
    last_name: str
    phone_number: str
    day_birthday: str
    is_active: bool

    class Config():
