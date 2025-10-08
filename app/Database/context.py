# app/Database/context.py
import sqlite3

class DbContext:
    _instance = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            if db_path is None:
                raise ValueError("DbContext must be initialized with db_path the first time.")
            cls._instance = super().__new__(cls)
            cls._instance._initialize(db_path)
        return cls._instance

    def _initialize(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON;")
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
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS otps (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        member_id INTEGER NOT NULL,
                        otp TEXT NOT NULL,
                        expires_at INTEGER NOT NULL,   -- epoch seconds
                        channel TEXT,                  -- "SMS" | "EMAIL" | "WEB" etc.
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(member_id),
                        FOREIGN KEY (member_id) REFERENCES users(id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise ValueError("DbContext has not been initialized. Initialize it first in app/__init__.py.")
        return cls._instance

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            DbContext._instance = None
