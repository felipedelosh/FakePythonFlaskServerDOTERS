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
        self.create_tables()

    def create_tables(self):
        try:
            with self.conn:
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        language TEXT NOT NULL,
                        enrollingSponsor TEXT NOT NULL,
                        enrollingChannel TEXT NOT NULL,
                        phoneNumber TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        activationUrl TEXT NOT NULL,
                        subscribeToNotifications INTEGER NOT NULL DEFAULT 1 CHECK (subscribeToNotifications IN (0,1)),
                        firstName TEXT NOT NULL,
                        lastName TEXT NOT NULL,
                        title TEXT,
                        dateOfBirth TEXT,
                        gender TEXT NOT NULL,
                        residentCountry TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                # self.conn.execute('''
                #     CREATE TABLE IF NOT EXISTS ??? (
                #         ...
                #     )
                # ''')
                self.conn.commit()
        except sqlite3.Error as e:
            pass

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            DbContext._instance = None
