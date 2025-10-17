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
