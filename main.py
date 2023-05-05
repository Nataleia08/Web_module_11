from sqlalchemy.orm import Session
from fastapi import FastAPI, Path, Query, Depends, HTTPException, status

from schemas import UserResponse, UserModel
from db import get_db
from models import User
from datetime import datetime, timedelta
from repository.users import birthday_in_this_year
from typing import List

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to API!"}

# @app.get("/api/healthchecker")
# def healthchecker(db: Session = Depends(get_db)):
#     try:
#         # Make request
#         result = db.execute("SELECT 1").fetchone()
#         if result is None:
#             raise HTTPException(status_code=500, detail="Database is not configured correctly")
#         return {"message": "Welcome to API!"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.post("/users", response_model=UserResponse, tags=["users"])
async def create_user(body:UserModel, db:Session = Depends(get_db)):
    user = db.query(User).filter_by(email = body.email).first()
    if user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "This email is exists!")
    user = User(**body.dict())
    user.birthday_now = birthday_in_this_year(user.day_birthday)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users", response_model=List[UserResponse], tags=["users"])
async def read_users(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def read_user(user_id: int = Path(description="The ID of the user", ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return user

@app.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(body:UserModel, user_id: int = Path(description="The ID of the user", ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    user.email = body.email
    db.commit()
    db.refresh(user)
    return user

@app.patch("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(body:UserModel, user_id: int = Path(description="The ID of the user", ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    user.email = body.email
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int = Path(description="The ID of the user", ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    db.delete(user)
    db.commit()


@app.get("/birthdays", tags=["birthday"])
async def read_users(days:int = 7, db: Session = Depends(get_db)):
    list_users = []
    for i in range(days):
        new_days = (datetime.now() + timedelta(days=i)).date()
        users = db.query(User).filter(User.birthday_now == new_days).all()
        list_users.append(users)
    return list_users


@app.get("/search/email", response_model=List[UserResponse], tags=["search"])
async def search_users(email: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.email == email).all()
    return users

@app.get("/search/first_name", response_model=List[UserResponse], tags=["search"])
async def search_users(first_name: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.first_name == first_name).all()
    return users

@app.get("/search/last_name", response_model=List[UserResponse], tags=["search"])
async def search_users(last_name: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.last_name == last_name).all()
    return users

@app.get("/search", response_model=List[UserResponse], tags=["search"])
async def search_users(email: str, first_name: str, last_name: str, db: Session = Depends(get_db)):
    users = db.query(User).filter((User.email == email) and (User.last_name == last_name) and (User.first_name == first_name)).all()
    return users