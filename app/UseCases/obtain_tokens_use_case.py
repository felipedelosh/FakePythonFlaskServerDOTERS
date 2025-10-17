# app/UseCases/obtain_tokens_use_case.py
from app.services.user_service import UserService
from app.services.member_callback_redirect_service import MemberCallbackRedirectService

class ObtainTokens:
    def __init__(self, callback_service: MemberCallbackRedirectService, user_service: UserService):
        self.callback_service = callback_service
        self.user_service = user_service

    def execute(self, params):
        print(params)

        return True
