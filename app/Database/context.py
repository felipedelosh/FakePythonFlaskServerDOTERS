# app/Database/context.py
import sqlite3

class DbContext:
    _instance = None

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(db_path)
        return cls._instance

    def _initialize(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            DbContext._instance = None
