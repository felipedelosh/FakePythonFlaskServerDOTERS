# app/services/accrual_service.py
from typing import Dict, Any, Optional
from app.models.MemberTransactionAccrual import MemberTransactionAccrual
from app.repositories.member_transactions_accrual_repository import MemberTransactionsAccrualRepository


class AccrualService:
    def __init__(self, accrual_repo: Optional[MemberTransactionsAccrualRepository] = None):
        self.accrual_repo = accrual_repo or MemberTransactionsAccrualRepository()

    def save_transaction(self, txn: MemberTransactionAccrual) -> Optional[Dict[str, Any]]:
        return self.accrual_repo.save(txn)
