# app\controllers\sso_member_callback_redirect_register.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.member_callback_redirect_repository import MemberCallbackRedirectRepository
from app.services.member_callback_redirect_service import MemberCallbackRedirectService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.UseCases.sso_member_callback_redirect_register_use_case import MemberCallbackRedirectRegister


def sso_member_callback_redirect_register():
    try:
        payload = request.get_json(force=True)
        user_repo = UserRepository()
        user_service = UserService(user_repo)
        callback_repo = MemberCallbackRedirectRepository()
        callback_service = MemberCallbackRedirectService(callback_repo)
        use_case = MemberCallbackRedirectRegister(callback_service, user_service)

        response = use_case.execute(payload)

        if not response:
            return error_response("CALLBACK REGISTER", "SERVER_ERROR", 400)

        return success_response(response, 200)
    except:
        return error_response("CALLBACK REGISTER", "SERVER_ERROR", 500)
