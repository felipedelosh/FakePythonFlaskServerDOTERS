# app/controllers/singup_controller.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.singup_repository import SingupRepository
from app.services.singup_service import SingupService
from app.UseCases.singup_use_case import SingupUseCase

def user_singup():
    try:
        payload = request.get_json(force=True)
        repo = SingupRepository()
        service = SingupService(repo)
        use_case = SingupUseCase(service)

        response = use_case.execute(payload)

        print(response)
        return success_response("SINGUP", 200)
    except:
        return error_response("SINGUP", "SERVER_ERROR", 500)