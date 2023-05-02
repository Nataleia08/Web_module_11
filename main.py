from sqlalchemy.orm import Session
from fastapi import FastAPI, Path, Query, Depends, HTTPException, status

from schemas import UserResponse, UserModel
from db import get_db
from models import User

app = FastAPI()

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute("SELECT 1").fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.post("/users", response_model=UserResponse)
async def create_user(body:UserModel, db:Session = Depends(get_db)):
    user = db.query(User).filter_by(email = body.email).first()
    if user:
        raise HTTPExeption(status_code = status.HTTP_409_CONFLICT, detail = "This email is exists!")
    user = User(email = body.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users")
async def read_users(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}")
async def read_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return user

@app.put("/users/{user_id}")
async def update_user(body:UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    user.email = body.email
    db.commit()
    db.refresh(user)
    return user

@app.patch("/users/{user_id}")
async def update_user(body:UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    user.email = body.email
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    db.delete(user)
    db.commit()