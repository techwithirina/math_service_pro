# db.py
import sqlite3
from datetime import datetime

DB_NAME = "requests.db"


def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            input TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def log_request(operation: str, input_data: str, result: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (operation, input, result, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (operation, input_data, result, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def get_requests_array():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM requests ORDER BY timestamp DESC''')
    rows = cursor.fetchall()  # This returns a list of tuples

    conn.close()
    return rows  # rows is your array (list of tuples)
