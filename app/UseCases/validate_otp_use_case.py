# app/UseCases/validate_otp_use_case.py
import time
from app.services.otps_service import OtpsService
from app.services.user_service import UserService
from app.models.Otp import Otp

class ValidateOtp:
    def __init__(self, otp_service: OtpsService, user_service: UserService):
        self.otp_service = otp_service
        self.user_service = user_service

    def execute(self, payload: dict):
        required_fields = ["memberId", "otp", "operation"]
        for field in required_fields:
            if field not in payload:
                return None
            
        usr = self.user_service.get_user_by_id(payload.get("memberId"))
        if not usr:
            return None
            
        request = self.otp_service.get_otp(payload.get("memberId"), payload.get("otp"), payload.get("operation"))

        if not request:
            return None
        
        now = int(time.time())
        _valid = False
        for i in request:
            if i.expires_at >= now:
                _valid = True
                break
        
        if not _valid:
            return None

        response = {
            "status": "Otp is valid and validation succeeded"
        }

        return response
