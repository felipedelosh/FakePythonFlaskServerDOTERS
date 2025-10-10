# app/UseCases/generate_otp_use_case.py
from app.services.otps_service import OtpsService

class GenerateOtp:
    def __init__(self, otp_service: OtpsService):
        self.otp_service = otp_service

    def execute(self, payload: dict):
        print(payload)

        return "loco"
