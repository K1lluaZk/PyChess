"""Database initialization and connection management."""
import os
import sqlite3
from typing import Optional
from contextlib import contextmanager

from config.settings import BASE_DIR

DB_FILE = os.path.join(BASE_DIR, "pychess.db")


class Database:
    """Manages SQLite database connection and table migrations."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DB_FILE
        self._is_memory = (self.db_path == ":memory:")
        self._memory_conn: Optional[sqlite3.Connection] = None
        if self._is_memory:
            # Maintain open reference for shared in-memory DB during tests
            self._memory_conn = sqlite3.connect("file:pychess_mem?mode=memory&cache=shared", uri=True)
            self._memory_conn.row_factory = sqlite3.Row
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Context manager yielding a database connection and ensuring closure."""
        if self._is_memory:
            conn = sqlite3.connect("file:pychess_mem?mode=memory&cache=shared", uri=True)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()

    def _init_db(self) -> None:
        """Initializes database schema if tables do not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                    points INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS match_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    winner TEXT NOT NULL,
                    points_earned INTEGER DEFAULT 0,
                    moves_count INTEGER DEFAULT 0,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                );
            """)
            conn.commit()
