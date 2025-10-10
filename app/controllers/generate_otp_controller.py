# app/controllers/generate_otp_controller.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.user_repository import UserRepository
from app.repositories.otps_repository import OtpsRepository
from app.services.otps_service import OtpsService
from app.services.user_service import UserService
from app.UseCases.generate_otp_use_case import GenerateOtp

def generate_otp():
    try:
        payload = request.get_json(force=True)

        otp_repo = OtpsRepository()
        otp_service = OtpsService(otp_repo)
        usr_repo = UserRepository()
        usr_service = UserService(usr_repo)
        use_case = GenerateOtp(otp_service, usr_service)

        req = use_case.execute(payload)

        if not req:
            return error_response("Bad Request Exception", "BAD_REQUEST", 400)

        return success_response(req, 200)
    except:
        return error_response("Bad Request Exception", "BAD_REQUEST", 400)
