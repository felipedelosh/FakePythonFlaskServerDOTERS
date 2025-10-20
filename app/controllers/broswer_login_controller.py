# app/controllers/broswer_login_controler.py
from flask import render_template, request, redirect
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from app.helpers.response import error_response
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.login_repository import LoginRepository
from app.services.login_service import LoginService
from app.services.refresh_token_service import RefreshTokenService
from app.UseCases.login_use_case import LoginUseCase
from app.helpers.fakeTokenizer import create_id_token
from app.helpers.fakeTokenizer import create_access_token
from app.helpers.fakeTokenizer import create_refresh_token
from app.models.RefreshToken import RefreshToken

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
        
        user_row = repo.get_by_email(email)
        uid = str(user_row["id"])
        full_name = f'{user_row.get("firstName","")} {user_row.get("lastName","")}'.strip() or email
        client_id = request.form.get("clientId") or request.args.get("clientId") or "doters-app"

        id_token = create_id_token(
            {"sub": email, "email": email, "uid": uid, "name": full_name, "role": "member"},
            client_id=client_id,
            ttl_seconds=60*60*6
        )

        access_token = create_access_token(
            subject=email,
            client_id=client_id,
            scope=["openid", "offline_access", "email", "profile"],
            ttl_seconds=60*60,
            extra_claims={"uid": uid, "role": "member"}
        )

        refresh_token = create_refresh_token(32)
        refresh_token_repository = RefreshTokenRepository()
        refresh_token_service = RefreshTokenService(refresh_token_repository)
        refresh_token_entity = RefreshToken(uid, refresh_token)

        data = {
            "access_token": access_token,
            "expires_in": "86400",
            "id_token": id_token,
            "refresh_token": refresh_token,
            "scope": "openid offline_access email profile",
            "token_type": "Bearer",
            "state": "12345"
        }

        refresh_token_service.save(refresh_token_entity)

        parsed = urlparse(redirect_uri)
        existing_qs = dict(parse_qsl(parsed.query, keep_blank_values=True))
        merged_qs = {**existing_qs, **data}
        new_query = urlencode(merged_qs, doseq=True)
        final_url = urlunparse(parsed._replace(query=new_query))

        return redirect(final_url, code=302)
    except:
        return error_response("Server Error", "INTERNAL_ERROR", 500)
