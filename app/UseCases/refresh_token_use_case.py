# app/UseCases/refresh_token_use_case.py
from flask import jsonify
from app.helpers.fakeTokenizer import create_id_token, create_access_token, verify_token, decode_token, create_refresh_token
from app.services.refresh_token_service import RefreshTokenService
from app.services.user_service import UserService

class RefreshTokenUseCase:
    def __init__(self, serice_refesh_token: RefreshTokenService, user_service: UserService):
        self.serice_refesh_token = serice_refesh_token
        self.user_service = user_service

    def execute(self, refresh_token: str, grant_type: str, x_channel: str = None, authorization: str = None):
        if not refresh_token or grant_type != "refresh_token":
            return jsonify({"error": "invalid_request"}), 400

        refresh_token = self.serice_refesh_token.get_by_token(refresh_token)
        if not refresh_token:
            return jsonify({"error": "invalid_token"}), 401
        

        print(refresh_token.member_id)
        usr = self.user_service.get_user_by_id(str(refresh_token))
        #WIP: Refresh TOKEN
        print(usr)

        return jsonify("LOCO"), 200
