from sqlalchemy.orm import Session
from src.application.commands.create_user import CreateUserCommandHandler
from src.infrastructure.db.session import SessionLocal
from src.interfaces.schemas.auth import LoginRequest, TokenResponse
from src.interfaces.schemas.user import UserCreate, UserResponse

from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    handler = CreateUserCommandHandler(db)
    return handler.execute(user.username, user.email, user.password)


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    pass
