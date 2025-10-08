# app/repositories/login_repository.py
from typing import Optional
from app.Database.context import DbContext

class LoginRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def get_by_email(self, email: str) -> Optional[dict]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, email, password, firstName, lastName
            FROM users
            WHERE email = ?
            LIMIT 1
        """, (email,))
        row = cur.fetchone()
        if not row:
            return None
        cols = [c[0] for c in cur.description]
        return dict(zip(cols, row))

    def validate_credentials(self, email: str, password: str) -> bool:
        user = self.get_by_email(email)
        if not user:
            return False
        return user["password"] == password
