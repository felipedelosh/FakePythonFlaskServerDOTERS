# app/repositories/member_callback_redirect_repository.py
import sqlite3
from typing import Optional, Dict, Any
from app.models.MemberCallbackRedirect import MemberCallbackRedirect
from app.Database.context import DbContext


class MemberCallbackRedirectRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def save(self, callback: MemberCallbackRedirect) -> Optional[Dict[str, Any]]:
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO member_callback_redirect (
                    member_id,
                    callback_url
                )
                VALUES (?, ?)
            """, (
                callback.member_id,
                callback.callback_url
            ))
            self.conn.commit()

            return {
                "id": cur.lastrowid,
                "member_id": callback.member_id,
                "callback_url": callback.callback_url
            }

        except sqlite3.IntegrityError as e:
            return None
        except sqlite3.Error as e:
            return None

    def get_by_member_and_url(self, member_id: int, callback_url: str) -> Optional[Dict[str, Any]]:
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT
                    id,
                    member_id,
                    callback_url,
                    created_at
                FROM member_callback_redirect
                WHERE member_id = ? AND callback_url = ?
                LIMIT 1
            """, (member_id, callback_url))

            row = cur.fetchone()
            if not row:
                return None

            cols = [col[0] for col in cur.description]
            return dict(zip(cols, row))

        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None
