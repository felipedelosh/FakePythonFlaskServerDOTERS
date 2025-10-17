# app/controllers/broswer_login_controler.py
from flask import render_template, request, redirect
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from app.helpers.response import error_response
from app.repositories.login_repository import LoginRepository
from app.services.login_service import LoginService
from app.UseCases.login_use_case import LoginUseCase
from app.helpers.fakeTokenizer import create_token

def browser_login():
    return render_template("login.html")


def browser_login_post():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        redirect_uri = (request.form.get("redirectUri") or "").strip()

        if not redirect_uri:
             return error_response("NOT CALLBACK", "BAD_REQUEST", 401)

        if not email or not password:
            return error_response("NOT USR or PASS", "BAD_REQUEST", 400)

        repo = LoginRepository()
        service = LoginService(repo)
        use_case = LoginUseCase(service)

        response = use_case.execute(request.form)

        if not response:
            return error_response("INVALID USR AND PASS", "UNAUTHORIZED", 401)
        
        claims = {
            "sub": email,
            "email": email,
            "role": "member",
            "uid": str(repo.get_by_email(email)["id"])
        }
        id_token = create_token(claims)
        
        data = {
            "access_token": "sqY5n6QcgvSNX7lAf78d2A6hJxop-439Rhr0cqO4nuD",
            "expires_in": "86400",
            "id_token": id_token,
            "refresh_token": "0WsteyOWU14Ew-t-vf7KEKOg3SSr6ak1PJMWV9n8abg",
            "scope": "openid offline_access email profile",
            "token_type": "Bearer",
            "state": "12345"
        }

        parsed = urlparse(redirect_uri)
        existing_qs = dict(parse_qsl(parsed.query, keep_blank_values=True))
        merged_qs = {**existing_qs, **data}
        new_query = urlencode(merged_qs, doseq=True)
        final_url = urlunparse(parsed._replace(query=new_query))

        return redirect(final_url, code=302)
    except:
        return error_response("Server Error", "INTERNAL_ERROR", 500)
