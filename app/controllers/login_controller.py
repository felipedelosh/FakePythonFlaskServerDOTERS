# app/controllers/login_controller.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.login_repository import LoginRepository
from app.services.login_service import LoginService
from app.UseCases.login_use_case import LoginUseCase
from app.helpers.fakeTokenizer import create_token


def user_login():
    try:
        # WIP
        payload = request.get_json(force=True)
        repo = LoginRepository()
        service = LoginService(repo)
        use_case = LoginUseCase(service)

        response = use_case.execute(payload)

        if not response:
            return error_response("Bad Request Exception", "BAD_REQUEST", 400)
        
        email = payload.get("email")
        claims = {
            "sub": email,
            "email": email,
            "role": "member",
            "uid": str(repo.get_by_email(email)["id"])
        }
        token = create_token(claims)# default TTL = 6 hours

        return success_response({"token": token}, 200)
    except:
        return error_response("Bad Request Exception", "BAD_REQUEST", 400)
