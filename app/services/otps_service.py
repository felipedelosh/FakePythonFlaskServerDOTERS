# app/services/otps_service.py
from typing import Optional, Dict, List, Any
from app.models.Otp import Otp
from app.repositories.otps_repository import OtpsRepository

class OtpsService:
    def __init__(self, otps_repository: OtpsRepository):
        self.otps_repo = otps_repository

    def generate_otp(self, otp: Otp) -> Dict[str, Any]:
        return self.otps_repo.generate_otp(otp)

    def get_otp(self, member_id: int, otp: str, operation: str) -> Optional[List[Otp]]:
        return self.otps_repo.get_otp_by_member_id_and_otp(member_id, otp, operation)
