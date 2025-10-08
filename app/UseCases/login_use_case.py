# app/UseCases/login_use_case.py
from app.services.login_service import LoginService

class LoginUseCase:
    def __init__(self, service: LoginService):
        self.service = service

    def execute(self, payload: dict) -> bool:
        email = payload.get("email")
        password = payload.get("password")

        if not email or not password:
            return False
        
        isCredentialsValid = self.service.validate_credentials(email, password)

        return isCredentialsValid
