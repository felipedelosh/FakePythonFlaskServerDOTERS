# app/controllers/obtain_tokens_controller.py
from flask import request
from flask import render_template
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.member_callback_redirect_repository import MemberCallbackRedirectRepository
from app.services.member_callback_redirect_service import MemberCallbackRedirectService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.UseCases.obtain_tokens_use_case import ObtainTokens


def obtain_tokens():
    try:
        params = request.args.to_dict(flat=True)

        user_repo = UserRepository()
        user_service = UserService(user_repo)
        callback_repo = MemberCallbackRedirectRepository()
        callback_service = MemberCallbackRedirectService(callback_repo)
        use_case = ObtainTokens(callback_service, user_service)

        response = use_case.execute(params)
        if not response:
            return render_template("obtain_tokens_error.html")
        
        return render_template("obtain_tokens_error.html")
    except:
        return render_template("obtain_tokens_error.html")
