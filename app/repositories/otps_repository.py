# app/repositories/otps_repository.py
import time
from app.models.Otp import Otp
import sqlite3
from typing import Optional, Dict, Any
from app.Database.context import DbContext
from app.helpers.fakeOtpGenerator import generate_otp_code

class OtpsRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def generate_otp(self, otp: Otp) -> Dict[str, Any]:
        try:
            expires = int(time.time()) + 180
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO otps (
                    member_id, otp, expires_at, sendEmail, sendSMS, sendWhts,
                    enrollingSponsor, returnOtp, channel, operation,
                    maxRedemptionPoints, language, newPhone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(member_id)
                DO UPDATE SET
                    otp = excluded.otp,
                    expires_at = excluded.expires_at,
                    sendEmail = excluded.sendEmail,
                    sendSMS = excluded.sendSMS,
                    sendWhts = excluded.sendWhts,
                    enrollingSponsor = excluded.enrollingSponsor,
                    returnOtp = excluded.returnOtp,
                    channel = excluded.channel,
                    operation = excluded.operation,
                    maxRedemptionPoints = excluded.maxRedemptionPoints,
                    language = excluded.language,
                    newPhone = excluded.newPhone,
                    created_at = CURRENT_TIMESTAMP
            """, (
                otp.member_id,
                otp.otp,
                expires,
                int(otp.sendEmail),
                int(otp.sendSMS),
                int(otp.sendWhts),
                otp.enrollingSponsor,
                int(otp.returnOtp),
                otp.channel,
                otp.operation,
                otp.maxRedemptionPoints,
                otp.language,
                otp.newPhone
            ))
            self.conn.commit()

            return {
                "member_id": otp.member_id,
                "otp": otp.otp,
                "expires_at": expires,
                "channel": otp.channel
            }
        except sqlite3.IntegrityError as e:
            print(f"[DB ERROR] IntegrityError: {e}")
            return None
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None


    def get_otp_by_member_id_and_otp(self, member_id: int, otp: str, operation: str) -> Optional[list[Otp]]:
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT
                    id,
                    member_id,
                    otp,
                    expires_at,
                    sendEmail,
                    sendSMS,
                    sendWhts,
                    enrollingSponsor,
                    returnOtp,
                    channel,
                    operation,
                    maxRedemptionPoints,
                    language,
                    newPhone,
                    created_at
                FROM otps
                WHERE member_id = ? AND otp = ? AND operation = ?
            """, (int(member_id), str(otp), str(operation)))

            rows = cur.fetchall()
            if not rows:
                return None

            cols = [c[0] for c in cur.description]
            results: list[Otp] = []
            for row in rows:
                rowdict = dict(zip(cols, row))
                otp_obj = Otp(
                    member_id=int(rowdict.get("member_id", 0)),
                    sendEmail=bool(rowdict.get("sendEmail", 0)),
                    sendSMS=bool(rowdict.get("sendSMS", 0)),
                    sendWhts=bool(rowdict.get("sendWhts", 0)),
                    enrollingSponsor=int(rowdict.get("enrollingSponsor", 0)),
                    returnOtp=bool(rowdict.get("returnOtp", 0)),
                    channel=rowdict.get("channel", "WEB"),
                    operation=rowdict.get("operation", "Generic"),
                    maxRedemptionPoints=int(rowdict.get("maxRedemptionPoints", 0)),
                    language=rowdict.get("language", "es-MX"),
                    newPhone=rowdict.get("newPhone"),
                    otp=rowdict.get("otp"),
                    expires_at=rowdict.get("expires_at")
                )
                results.append(otp_obj)

            return results

        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None
