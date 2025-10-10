# app/controllers/validate_otp_controller.py
from flask import request
from app.repositories.otps_repository import OtpsRepository
from app.services.otps_service import OtpsService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.UseCases.validate_otp_use_case import ValidateOtp
from app.helpers.response import success_response
from app.helpers.response import unauthorized

def validate_otp():
    try:
        payload = request.get_json(force=True)
        otp_repo = OtpsRepository()
        otp_service = OtpsService(otp_repo)
        usr_repo = UserRepository()
        usr_service = UserService(usr_repo)
        use_case = ValidateOtp(otp_service, usr_service)

        req = use_case.execute(payload)

        if not req:
            return unauthorized()

        return success_response(req, 201)
    except:
        return unauthorized()
