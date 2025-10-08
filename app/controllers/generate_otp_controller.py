# app/controllers/generate_otp_controller.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.singup_repository import SingupRepository
from app.repositories.otps_repository import OtpsRepository
from app.services.otps_service import OtpsService
from app.UseCases.generate_otp_use_case import GenerateOtp

def generate_otp():
    try:
        payload = request.get_json(force=True)

        usr_repo = SingupRepository()
        otp_repo = OtpsRepository()
        service = OtpsService(otp_repo, usr_repo)
        use_case = GenerateOtp(service)

        req = use_case.execute(payload)
        return success_response(req, 200)
    except:
        return error_response("Bad Request Exception", "BAD_REQUEST", 400)
