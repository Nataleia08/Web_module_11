from pydantic import BaseModel, EmailStr, PastDate, Field

class UserModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    day_birthday: PastDate

class UserResponse(BaseModel):
    id: int = Field(default=1, ge=1)
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    day_birthday: PastDate
    is_active: bool

    class Config():
        orm_mode = True


