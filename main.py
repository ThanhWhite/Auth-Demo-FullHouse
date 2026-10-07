from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from dependencies import get_current_user
from models import User
from routers.auth import router as auth_router
from schemas import UserResponse
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Authentication Demo",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def home():

    return {
        "message": "FastAPI Auth API is running"
    }

@app.get(
    "/users",
    response_model=list[UserResponse],
    tags=["Users"]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(User).all()

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)