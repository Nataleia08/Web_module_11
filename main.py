from fastapi import FastAPI
from sqlalchemy.orm import Session

from schemas import UserResponse, UserModel

app = FastAPI()

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/api/healthchecker")
def healthchecker():
    pass

@app.post("/users", response_model=UserResponse)
async def create_user(body:UserModel, db:Session = Depends(get_db)):
    user = db.query(User).filter_by(email = body.email).first()
    if user:
        raise HTTPExeption(status_code = status.HTTP_409_CONFLICT)
    return {}

@app.get("/users")