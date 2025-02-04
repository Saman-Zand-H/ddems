from infrastructure.email.smtp_client import EmailClient
from sqlalchemy.orm import Session
from src.domain.models.user import User


class CreateUserCommandHandler:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.email_client = EmailClient()

    def execute(self, username: str, email: str, hashed_password: str):
        user = User(username=username, email=email, hashed_password=hashed_password)
        self.db_session.add(user)
        self.db_session.commit()

        verification_link = f"http://example.com/verify-email?token={user.id}"
        self.email_client.send_verification_email(email, verification_link)

        return user
