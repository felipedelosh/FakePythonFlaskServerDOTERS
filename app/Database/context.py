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
                        expires_at INTEGER NOT NULL,         -- epoch seconds
                        sendEmail INTEGER NOT NULL DEFAULT 0 CHECK (sendEmail IN (0,1)),
                        sendSMS INTEGER NOT NULL DEFAULT 0 CHECK (sendSMS IN (0,1)),
                        sendWhts INTEGER NOT NULL DEFAULT 0 CHECK (sendWhts IN (0,1)),
                        enrollingSponsor INTEGER DEFAULT 0,
                        returnOtp INTEGER NOT NULL DEFAULT 0 CHECK (returnOtp IN (0,1)),
                        channel TEXT NOT NULL,
                        operation TEXT NOT NULL,
                        maxRedemptionPoints INTEGER DEFAULT 0,
                        language TEXT NOT NULL,
                        newPhone TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(member_id),
                        FOREIGN KEY (member_id) REFERENCES users(id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
                    );
                ''')
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS member_transactions_accrual (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hSponsorId INTEGER NOT NULL,
                        hBitType TEXT NOT NULL,
                        hBitCategory TEXT NOT NULL,
                        hMemberId INTEGER NOT NULL,
                        hBitDate TEXT NOT NULL,
                        hBitCurrency TEXT NOT NULL,
                        hBitAmount REAL NOT NULL,
                        hBitSourceGeneratedId TEXT NOT NULL,
                        taxAmount REAL,
                        processingDate TEXT,
                        pointsRewarded BOOLEAN DEFAULT 1,
                        pointsRedeemed BOOLEAN DEFAULT 0,
                        pointsReset BOOLEAN DEFAULT 0,
                        status TEXT DEFAULT 'SUCCESS',
                        bitId TEXT,
                        created_at TEXT DEFAULT (datetime('now')),
                        FOREIGN KEY (hMemberId) REFERENCES users(id)
                    );
                """)
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS member_callback_redirect (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        member_id INTEGER NOT NULL,
                        callback_url TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE (member_id, callback_url),
                        FOREIGN KEY (member_id) REFERENCES users(id)
                    )
                ''')
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS refresh_tokens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        memberId INTEGER NOT NULL,
                        refresh_token TEXT NOT NULL UNIQUE,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (memberId) REFERENCES users(id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
                        UNIQUE(memberId)
                    )
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
