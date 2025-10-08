# app/services/login_service.py
from app.repositories.login_repository import LoginRepository

class LoginService:
    def __init__(self, repository: LoginRepository):
        self.repository = repository

    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)

    def validate_credentials(self, email: str, password: str) -> bool:
        return self.repository.validate_credentials(email, password)
