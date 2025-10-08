# app/controllers/singup_controller.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.helpers.response import singup_error_duplicated
from app.helpers.response import singup_error_general
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


        if not response:
            return error_response("SINGUP", "SERVER_ERROR", 500)
        
        if response == -1:
            user = service.get_by_email(payload.get("email"))

            if not user:
                return error_response("SINGUP", "SERVER_ERROR", 500)
            
            user_id = user["id"]
            first_name = user["firstName"]
            last_name = user["lastName"]

            return singup_error_duplicated(user_id, first_name, last_name)

        if response <= -2:
            return singup_error_general("not defined", "required", 500)
        
        personal = payload.get("personalDetails")
        name = personal.get("name")
        data = {
            "navitaireStatus": "Created",
            "gravtyStatus": "Created",
            "customerNumber": response,
            "firstName": name.get("firstName"),
            "lastName": name.get("lastName")
        }

        return success_response(data, 200)
    except:
        return error_response("SINGUP", "SERVER_ERROR", 500)