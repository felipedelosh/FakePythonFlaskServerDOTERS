# app/UseCases/sso_member_callback_redirect_register_use_case.py
from app.services.member_callback_redirect_service import MemberCallbackRedirectService
from app.services.user_service import UserService
from app.models.MemberCallbackRedirect import MemberCallbackRedirect

class MemberCallbackRedirectRegister:
    def __init__(self, callback_service: MemberCallbackRedirectService, user_service: UserService):
        self.callback_service = callback_service
        self.user_service = user_service

    def execute(self, payload: dict):
        required_fields = [
            "memberId",
            "callbackUrl"
        ]

        for field in required_fields:
            if field not in payload:
                return None
        
        callback = MemberCallbackRedirect.from_payload(payload)

        usr = self.user_service.get_user_by_id(callback.member_id)
        if not usr:
            return None

        saved = self.callback_service.save_callback(callback)
        if not saved:
            return None


        return saved
