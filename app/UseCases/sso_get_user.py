# app/UseCases/sso_get_user.py
from flask import jsonify
from app.helpers.fakeTokenizer import verify_token, decode_token

class GetUserInfo:
    def __init__(self):
        pass

    def execute(self, x_chanel, sso_token):
        print(x_chanel)
        print(sso_token)

        token = sso_token.strip()
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1].strip()

        if not verify_token(token):
            return jsonify({"error": "Invalid or expired token"}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Malformed token"}), 400

        user_data = {
            "sub": payload.get("uid") or payload.get("sub"),
            "email": payload.get("email"),
            "first": payload.get("name", "").split(" ")[0] if payload.get("name") else None,
            "last": " ".join(payload.get("name", "").split(" ")[1:]) if payload.get("name") else None,
            "title": None
        }

        return jsonify(payload), 200
