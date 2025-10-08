# app/UseCases/generate_otp_use_case.py
from app.services.otps_service import OtpsService

class GenerateOtp:
    def __init__(self, otp_service: OtpsService):
        self.otp_service = otp_service

    def execute(self, payload: dict):
        required_fields = ["memberId", "channel", "operation"]
        for field in required_fields:
            if field not in payload or payload[field] in (None, "", []):
                raise ValueError(f"{field} is required")
            
        send_email = bool(payload.get("sendEmail", False))
        send_sms = bool(payload.get("sendSMS", False))
        return_otp = bool(payload.get("returnOtp", False))
        channel = payload.get("channel", "WEB")
        operation = payload.get("operation", "Generic")
        max_redemption_points = int(payload.get("maxRedemptionPoints", 0))

        try:
            member_id = int(payload["memberId"])
        except (ValueError, TypeError):
            raise ValueError("memberId must be numeric")

        otp_data = self.otp_service.issue_for_member(
            member_id=member_id,
            ttl_seconds=180,
            channel=channel
        )

        response = {
            "sentMail": "Email queued" if send_email else "Email not selected to send",
            "sentSms": "Sms queued" if send_sms else "Sms not selected to send"
        }

        if return_otp:
            response["otp"] = int(otp_data["otp"])

        return response
