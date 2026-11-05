import sqlite3
import os

DB_NAME = 'data.db'

def init_db():
    """Инициализирует базу данных и создаёт таблицу, если её нет."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL,  
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def get_db_connection():
    """Возвращает подключение к базе данных с поддержкой доступа по именам колонок."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
