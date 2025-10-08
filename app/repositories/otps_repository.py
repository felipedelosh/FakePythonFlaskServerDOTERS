# app/repositories/otps_repository.py
import time
from typing import Optional, Dict, Any
from app.Database.context import DbContext
from app.helpers.fakeOtpGenerator import generate_otp_code

class OtpsRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def issue_for_member(self, member_id: int, ttl_seconds: int = 180, channel: str = "WEB", length: int = 6) -> Dict[str, Any]:
        otp = generate_otp_code()
        expires = int(time.time()) + int(ttl_seconds)

        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO otps(member_id, otp, expires_at, channel)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(member_id)
            DO UPDATE SET otp=excluded.otp, expires_at=excluded.expires_at, channel=excluded.channel
        """, (member_id, otp, expires, channel))
        self.conn.commit()

        return {"member_id": member_id, "otp": otp, "expires_at": expires, "channel": channel}

    def validate(self, member_id: int, otp: str) -> bool:
        now = int(time.time())
        cur = self.conn.cursor()
        cur.execute("""
            SELECT otp FROM otps
            WHERE member_id = ? AND expires_at > ?
            LIMIT 1
        """, (member_id, now))
        row = cur.fetchone()
        if not row:
            return False
        ok = (row[0] == str(otp))
        if ok:
            cur.execute("DELETE FROM otps WHERE member_id = ?", (member_id,))
            self.conn.commit()
        return ok

    def cleanup_expired(self) -> int:
        now = int(time.time())
        cur = self.conn.cursor()
        cur.execute("DELETE FROM otps WHERE expires_at <= ?", (now,))
        self.conn.commit()
        return cur.rowcount
