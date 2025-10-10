# app/UseCases/generate_otp_use_case.py
from app.services.otps_service import OtpsService
from app.services.user_service import UserService
from app.models.Otp import Otp
from app.helpers.fakeOtpGenerator import generate_otp_code

class GenerateOtp:
    def __init__(self, otp_service: OtpsService, user_service: UserService):
        self.otp_service = otp_service
        self.user_service = user_service

    def execute(self, payload: dict):
        required_fields = ["memberId", "returnOtp", "operation"]
        for field in required_fields:
            if field not in payload:
                return None

        send_fields = ["sendEmail", "sendSMS", "sendWhts"]
        if not all(f in payload for f in send_fields):
            return None

        if not any(bool(payload.get(f)) for f in send_fields):
            return None
        
        otp_entity = Otp.from_payload(payload)
        otp_entity.otp = generate_otp_code()

        usr = self.user_service.get_user_by_id(otp_entity.member_id)
        if not usr:
            return None

        result = self.otp_service.generate_otp(otp_entity)
        if not result:
            raise ValueError("Error generating OTP in database")
        
        response = {
            "sentMail": "Email queued" if otp_entity.sendEmail else "Email not selected to send",
            "sentSms": "Sms queued" if otp_entity.sendSMS else "Sms not selected to send",
            "sentWhts": "WhatsApp queued" if otp_entity.sendWhts else "WhatsApp not selected to send",
        }
        
        if otp_entity.returnOtp:
            response["otp"] = int(otp_entity.otp)

        return response
