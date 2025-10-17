# app/UseCases/obtain_tokens_use_case.py
from app.services.user_service import UserService
from app.services.member_callback_redirect_service import MemberCallbackRedirectService
from app.services.login_service import LoginService

class ObtainTokens:
    def __init__(self, callback_service: MemberCallbackRedirectService, user_service: UserService, login_service: LoginService):
        self.callback_service = callback_service
        self.user_service = user_service
        self.login_service = login_service

    def execute(self, params: dict):
        required_fields = [
            "clientId",
            "clientSecret",
            "language",
            "redirectUri",
            "state"
        ]

        missing = [field for field in required_fields if not params.get(field)]
        if missing:
            return None
        
        usr = self.user_service.get_user_by_id(params["clientId"])
        if not usr:
            return None

        isCredentialsValid = self.login_service.validate_credentials(usr["email"], params["clientSecret"])
        if not isCredentialsValid:
            return False

        return True
