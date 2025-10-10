# app/repositories/user_repository.py
from app.Database.context import DbContext

class UserRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def get_user_by_id(self, user_id: int):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        columns = [col[0] for col in cur.description]
        return dict(zip(columns, row))
