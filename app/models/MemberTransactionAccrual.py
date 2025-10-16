# app/models/MemberTransactionAccrual.py
from typing import Optional
from datetime import datetime
import random
import string


class MemberTransactionAccrual:
    def __init__(
        self,
        hSponsorId: int,
        hBitType: str,
        hBitCategory: str,
        hMemberId: int,
        hBitDate: str,
        hBitCurrency: str,
        hBitAmount: float,
        hBitSourceGeneratedId: str,
        taxAmount: Optional[float] = None,
        processingDate: Optional[str] = None,
        pointsRewarded: bool = True,
        pointsRedeemed: bool = False,
        pointsReset: bool = False,
        status: str = "SUCCESS",
        bitId: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.hSponsorId = hSponsorId
        self.hBitType = hBitType
        self.hBitCategory = hBitCategory
        self.hMemberId = hMemberId
        self.hBitDate = hBitDate
        self.hBitCurrency = hBitCurrency
        self.hBitAmount = hBitAmount
        self.hBitSourceGeneratedId = hBitSourceGeneratedId
        self.taxAmount = taxAmount
        self.processingDate = processingDate or datetime.utcnow().isoformat()
        self.pointsRewarded = pointsRewarded
        self.pointsRedeemed = pointsRedeemed
        self.pointsReset = pointsReset
        self.status = status
        self.bitId = bitId or self._generate_bit_id()
        self.created_at = created_at or datetime.utcnow().isoformat()

    @classmethod
    def from_payload(cls, payload: dict):
        return cls(
            hSponsorId=int(payload.get("hSponsorId", 0)),
            hBitType=payload.get("hBitType", "DELIVERY"),
            hBitCategory=payload.get("hBitCategory", "ACCRUAL"),
            hMemberId=int(payload.get("hMemberId", 0)),
            hBitDate=payload.get("hBitDate", datetime.utcnow().isoformat()),
            hBitCurrency=payload.get("hBitCurrency", "MXN"),
            hBitAmount=float(payload.get("hBitAmount", 0)),
            hBitSourceGeneratedId=payload.get("hBitSourceGeneratedId", ""),
            taxAmount=float(payload.get("taxAmount", 0)),
        )

    def _generate_bit_id(self, length: int = 27) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choices(chars, k=length))

    def to_dict(self):
        return {
            "hSponsorId": self.hSponsorId,
            "hBitType": self.hBitType,
            "hBitCategory": self.hBitCategory,
            "hMemberId": self.hMemberId,
            "hBitDate": self.hBitDate,
            "hBitCurrency": self.hBitCurrency,
            "hBitAmount": self.hBitAmount,
            "hBitSourceGeneratedId": self.hBitSourceGeneratedId,
            "taxAmount": self.taxAmount,
            "processingDate": self.processingDate,
            "pointsRewarded": self.pointsRewarded,
            "pointsRedeemed": self.pointsRedeemed,
            "pointsReset": self.pointsReset,
            "status": self.status,
            "bitId": self.bitId,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return (
            f"<MemberTransactionAccrual "
            f"member_id={self.hMemberId} amount={self.hBitAmount} currency={self.hBitCurrency}>"
        )
