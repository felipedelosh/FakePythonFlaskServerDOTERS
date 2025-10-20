# app\controllers\refresh_token_controller.py
from flask import request
from app.helpers.response import error_response
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.refresh_token_service import RefreshTokenService
from app.UseCases.refresh_token_use_case import RefreshTokenUseCase
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

def refresh_token():
    try:
        x_channel = request.headers.get("X-Channel")
        authorization = request.headers.get("Authorization")
        refresh_token = request.form.get("refresh_token")
        grant_type = request.form.get("grant_type")

        repo_refresh_token = RefreshTokenRepository()
        service_refresh_token = RefreshTokenService(repo_refresh_token)
        repo_user = UserRepository()
        service_user = UserService(repo_user)
        use_case = RefreshTokenUseCase(service_refresh_token, service_user)

        return use_case.execute(refresh_token=refresh_token, grant_type=grant_type, x_channel=x_channel, authorization=authorization)
    except:
        return error_response("Server Error", "INTERNAL_ERROR", 500)
