# app/services/otps_service.py
from typing import Optional, Dict, Any
from app.repositories.otps_repository import OtpsRepository
from app.repositories.singup_repository import SingupRepository

class OtpsService:
    def __init__(self, otps_repository: OtpsRepository, users_repository: SingupRepository):
        self.otps_repo = otps_repository
        self.users_repo = users_repository

    def issue_for_member(self, member_id: int, ttl_seconds: int = 180, channel: str = "WEB", length: int = 6) -> Dict[str, Any]:
        return self.otps_repo.issue_for_member(member_id, ttl_seconds, channel, length)

    def issue_for_email(self, email: str, ttl_seconds: int = 180, channel: str = "WEB", length: int = 6) -> Optional[Dict[str, Any]]:
        user = self.users_repo.get_by_email(email)
        if not user:
            return None
        member_id = int(user["id"])
        return self.issue_for_member(member_id, ttl_seconds, channel, length)

    def validate(self, member_id: int, otp: str) -> bool:
        return self.otps_repo.validate(member_id, otp)

    def cleanup_expired(self) -> int:
        return self.otps_repo.cleanup_expired()
