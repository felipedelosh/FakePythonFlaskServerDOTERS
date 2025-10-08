# app/repositories/singup_repository.py
import sqlite3
from app.Database.context import DbContext
from app.models.User import User

class SingupRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def get_by_email(self, email: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        if not row:
            return None
        cols = [c[0] for c in cur.description]
        return dict(zip(cols, row))

    def create(self, user: User) -> int:
        cur = self.conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (
                    language, enrollingSponsor, enrollingChannel,
                    phoneNumber, email, password, activationUrl,
                    subscribeToNotifications, firstName, lastName, title,
                    dateOfBirth, gender, residentCountry
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                user.language,
                user.enrollingSponsor,
                user.enrollingChannel,
                user.phoneNumber,
                user.email,
                user.password,
                user.activationUrl,
                1 if user.subscribeToNotifications else 0,
                user.firstName,
                user.lastName,
                user.title,
                user.dateOfBirth,
                user.gender,
                user.residentCountry
            ))
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            # Duplicated EMAIL
            return -1
        except sqlite3.Error:
            return -2
