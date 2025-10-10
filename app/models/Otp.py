# app/models/Otp.py
from typing import Optional

class Otp:
    def __init__(
        self,
        member_id: int,
        sendEmail: bool,
        sendSMS: bool,
        sendWhts: bool,
        enrollingSponsor: int,
        returnOtp: bool,
        channel: str,
        operation: str,
        maxRedemptionPoints: int,
        language: str,
        newPhone: Optional[str] = None,
        otp: Optional[str] = None,
        expires_at: Optional[int] = None,
    ):
        self.member_id = member_id
        self.sendEmail = sendEmail
        self.sendSMS = sendSMS
        self.sendWhts = sendWhts
        self.enrollingSponsor = enrollingSponsor
        self.returnOtp = returnOtp
        self.channel = channel
        self.operation = operation
        self.maxRedemptionPoints = maxRedemptionPoints
        self.language = language
        self.newPhone = newPhone
        self.otp = otp
        self.expires_at = expires_at

    @classmethod
    def from_payload(cls, payload: dict):
        """Construye un objeto Otp a partir del request JSON."""
        return cls(
            member_id=int(payload.get("memberId", 0)),
            sendEmail=bool(payload.get("sendEmail", False)),
            sendSMS=bool(payload.get("sendSMS", False)),
            sendWhts=bool(payload.get("sendWhts", False)),
            enrollingSponsor=int(payload.get("enrollingSponsor", 0)),
            returnOtp=bool(payload.get("returnOtp", False)),
            channel=payload.get("channel", "WEB"),
            operation=payload.get("operation", "Generic"),
            maxRedemptionPoints=int(payload.get("maxRedemptionPoints", 0)),
            language=payload.get("language", "es-MX"),
            newPhone=payload.get("newPhone"),
        )

    def __repr__(self):
        return f"<Otp member_id={self.member_id} channel={self.channel}>"
