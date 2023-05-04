from pydantic import BaseModel, EmailStr, PastDate

class UserModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    day_birthday: PastDate

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    day_birthday: str
    is_active: bool

    class Config():
        pass


