# app/repositories/otps_repository.py
import time
from typing import Optional, Dict, Any
from app.Database.context import DbContext
from app.helpers.fakeOtpGenerator import generate_otp_code

class OtpsRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def generate_otp(self) -> Dict[str, Any]:
        pass

    def get_otp_by_member_id_and_otp(self) -> Optional[Dict[str, Any]]:
        pass
