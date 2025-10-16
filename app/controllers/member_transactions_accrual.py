# app/controllers/member_transactions_accrual.py
from flask import request
from app.helpers.response import success_response
from app.helpers.response import error_response
from app.repositories.member_transactions_accrual_repository import MemberTransactionsAccrualRepository
from app.repositories.user_repository import UserRepository
from app.services.accrual_service import AccrualService
from app.services.user_service import UserService
from app.UseCases.accrual_use_case import AccrualUseCase

def member_transactions_accural():
    try:
        payload = request.get_json(force=True)
        repo_aku = MemberTransactionsAccrualRepository()
        repo_usr = UserRepository()
        service_aku = AccrualService(repo_aku)
        service_usr = UserService(repo_usr)
        use_case = AccrualUseCase(service_aku, service_usr)
        
        req = use_case.execute(payload)
    
        if not req:
            return error_response("Bad request", "BAD_REQUEST", 400)

        return success_response(req, 200)
    except:
        return error_response("Server Error", "BAD_REQUEST", 500)
