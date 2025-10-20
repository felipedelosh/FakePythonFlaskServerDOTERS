# app/controllers/sso_user_controller.py
from flask import request
from app.helpers.response import error_response

from app.UseCases.sso_get_user import GetUserInfo

def get_user_info():
    try:
        x_chanel = request.headers.get("X-Channel")
        sso_token = request.headers.get("Authorization")

        use_case = GetUserInfo()

        response = use_case.execute(x_chanel, sso_token)

        if not response:
            return error_response("SSO", "BAD_REQUEST", 400)

        return response
    except:
        return error_response("USER INFO", "SERVER_ERROR", 500)
