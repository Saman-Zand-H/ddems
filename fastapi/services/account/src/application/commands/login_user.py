# src/application/commands/login_user.py
from domain.services.auth import AuthService
from interfaces.exceptions.auth_exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session
from src.domain.models.user import User


class LoginUserCommandHandler:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def execute(self, username: str, password: str):
        user = self.db_session.query(User).filter(User.username == username).first()
        if not user or not AuthService.check_password(password, user.hashed_password):
            raise InvalidCredentialsException()

        token_data = {"sub": user.username}
        token = AuthService.create_access_token(token_data)
        return token
