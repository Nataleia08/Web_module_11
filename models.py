from sqlalchemy import Boolean, Column, func, DateTime, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from db import Base, engine
from repository.users import birthday_in_this_year

# Ім'я
# Прізвище
# Електронна адреса
# Номер телефону
# День народження
# Додаткові дані (необов'язково)

class User(Base):
    __tablename__ = "users"

    id = Column('id',Integer, primary_key = True, index = True)
    first_name = Column('first_name', String(length=50))
    last_name = Column('last_name',String(length=50))
    email = Column('email', String(length=150), unique=True)
    phone_number = Column('phone', String(length=150))
    day_birthday = Column('birthday', Date)
    # birthday_now = Column(Date, default=birthday_in_this_year(day_birthday))
    hashed_password = Column('password', String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base.metadata.create_all(bind=engine)
