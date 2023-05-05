from pydantic import BaseModel, EmailStr, PastDate, Field, FutureDate
from datetime import datetime, date
from typing import Optional

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
    birthday_now: date
    is_active: bool
    created_at: datetime
    update_at: datetime

    class Config():
        orm_mode = True
