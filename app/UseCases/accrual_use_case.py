# app/UseCases/accrual_use_case.py
from app.models.MemberTransactionAccrual import MemberTransactionAccrual
from app.services.accrual_service import AccrualService
from app.services.user_service import UserService


class AccrualUseCase:
    def __init__(self, service_aku: AccrualService, user_service: UserService):
        self.service_aku = service_aku
        self.user_service = user_service

    def execute(self, payload: dict):
        required_fields = [
            "hSponsorId",
            "hBitType",
            "hBitCategory",
            "hMemberId",
            "hBitDate",
            "hBitCurrency",
            "hBitAmount",
            "hBitSourceGeneratedId",
            "taxAmount"
        ]

        for field in required_fields:
            if field not in payload:
                return None
            
        txn = MemberTransactionAccrual.from_payload(payload)

        if txn.hBitType != "DELIVERY" or txn.hBitCategory != "ACCRUAL":
            return None

        usr = self.user_service.get_user_by_id(txn.hMemberId)
        if not usr:
            return None
        
        saved = self.service_aku.save_transaction(txn)
        if not saved:
            return None

        old_balance = 0
        rewarded = int(round(txn.hBitAmount))

        data = {
            "LoyaltyBalances": [
                {
                    "loyaltyAccountId": "4",
                    "redeemed": 0,
                    "oldBalance": old_balance,
                    "newBalance": old_balance + rewarded,
                    "rewarded": rewarded
                }
            ],
            "processingDate": txn.processingDate,
            "bitId": txn.bitId,
            "pointsRewarded": True,
            "pointsRedeemed": False,
            "pointsReset": False,
            "status": "SUCCESS",
            "error": None,
            "memberId": str(txn.hMemberId)
        }

        return data
