from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db import Base, engine

# Ім'я
# Прізвище
# Електронна адреса
# Номер телефону
# День народження
# Додаткові дані (необов'язково)

class User():
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    firs_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String)
    day_birthday = Column(DateTime)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)
