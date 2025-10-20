# app/repositories/refresh_token_repository.py
import sqlite3
from typing import Optional
from app.Database.context import DbContext
from app.models.RefreshToken import RefreshToken

class RefreshTokenRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def save_refresh_token(self, refresh_token: RefreshToken) -> bool:
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO refresh_tokens (memberId, refresh_token, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(memberId)
                DO UPDATE SET
                    refresh_token = excluded.refresh_token,
                    created_at = CURRENT_TIMESTAMP
            """, (refresh_token.member_id, refresh_token.refresh_token, refresh_token.created_at))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return False

    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT memberId, refresh_token, created_at FROM refresh_tokens WHERE refresh_token = ?", (token,))
            row = cur.fetchone()
            if row:
                keys = ["memberId", "refresh_token", "created_at"]
                data = dict(zip(keys, row))
                return RefreshToken.from_row(data)
            return None
        except sqlite3.Error as e:
            return None
