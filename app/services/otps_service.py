# app/services/otps_service.py
from typing import Optional, Dict, Any
from app.repositories.otps_repository import OtpsRepository
from app.repositories.singup_repository import SingupRepository

class OtpsService:
    def __init__(self, otps_repository: OtpsRepository, users_repository: SingupRepository):
        self.otps_repo = otps_repository
        self.users_repo = users_repository

    def generate_otp(self) -> Dict[str, Any]:
        return self.otps_repo.generate_otp()

    def get_otp(self, member_id: int, otp: str) -> Optional[Dict[str, Any]]:
        return self.otps_repo.get_otp_by_member_id_and_otp()
