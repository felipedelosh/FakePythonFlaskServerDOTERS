# app/services/singup_service.py
from app.repositories.singup_repository import SingupRepository
from app.models.User import User

class SingupService:
    def __init__(self, repository: SingupRepository):
        self.repository = repository

    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)

    def create(self, user: User) -> int:
        return self.repository.create(user)
