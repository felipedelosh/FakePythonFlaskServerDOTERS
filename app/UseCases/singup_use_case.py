# app/UseCases/singup_use_case.py
from app.services.singup_service import SingupService
from app.models.User import User

class SingupUseCase:
    def __init__(self, service: SingupService):
        self.service = service

    def execute(self, payload: dict):
        user = User.from_payload(payload)
        user_id = self.service.create(user)
        return user_id