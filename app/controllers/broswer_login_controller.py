# app/controllers/broswer_login_controler.py
from flask import render_template, request
from app.helpers.response import success_response, error_response
from app.repositories.login_repository import LoginRepository
from app.services.login_service import LoginService
from app.UseCases.login_use_case import LoginUseCase

def browser_login():
    return render_template("login.html")


def browser_login_post():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return error_response("Campos requeridos", "BAD_REQUEST", 400)

        repo = LoginRepository()
        service = LoginService(repo)
        use_case = LoginUseCase(service)

        response = use_case.execute(request.form)

        if not response:
            return error_response("Credenciales inválidas", "UNAUTHORIZED", 401)
        
        data = {
            "access_token": "sqY5n6QcgvSNX7lAf78d2A6hJxop-439Rhr0cqO4nuD",
            "expires_in": "86400",
            "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6...",
            "refresh_token": "0WsteyOWU14Ew-t-vf7KEKOg3SSr6ak1PJMWV9n8abg",
            "scope": "openid offline_access email profile",
            "token_type": "Bearer",
            "state": "12345"
        }

        return success_response(data, 200)
    except:
        return error_response("Server Error", "INTERNAL_ERROR", 500)
