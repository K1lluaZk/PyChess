"""Repository layer for user accounts and score persistence."""
from typing import List, Optional

from database.db import Database
from database.models import User


class UserRepository:
    """Provides CRUD and points operations for User entities."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Fetch a user account by case-insensitive username."""
        clean_name = username.strip()
        if not clean_name:
            return None

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, points, created_at FROM users WHERE username = ? COLLATE NOCASE",
                (clean_name,),
            )
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    username=row["username"],
                    points=row["points"],
                    created_at=str(row["created_at"]),
                )
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user account by user ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, points, created_at FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    username=row["username"],
                    points=row["points"],
                    created_at=str(row["created_at"]),
                )
            return None

    def create_user(self, username: str, initial_points: int = 0) -> Optional[User]:
        """Create a new user account. Returns None if username already exists."""
        clean_name = username.strip()
        if not clean_name:
            return None

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, points) VALUES (?, ?)",
                    (clean_name, initial_points),
                )
                user_id = cursor.lastrowid
                conn.commit()
                return self.get_user_by_id(user_id)
        except Exception:
            return None

    def get_or_create_user(self, username: str) -> Optional[User]:
        """Fetch existing user or create a new user account."""
        user = self.get_user_by_username(username)
        if user:
            return user
        return self.create_user(username)

    def add_points(self, user_id: int, points: int) -> int:
        """Add points to a user account and return their updated total points."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET points = points + ? WHERE id = ?",
                (points, user_id),
            )
            conn.commit()

        updated_user = self.get_user_by_id(user_id)
        return updated_user.points if updated_user else 0

    def get_top_players(self, limit: int = 10) -> List[User]:
        """Retrieve top players sorted by total points descending."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, points, created_at FROM users ORDER BY points DESC, id ASC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()
            return [
                User(
                    id=r["id"],
                    username=r["username"],
                    points=r["points"],
                    created_at=str(r["created_at"]),
                )
                for r in rows
            ]

    def record_match(self, user_id: Optional[int], winner: str, points_earned: int, moves_count: int) -> None:
        """Record a completed chess match."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO match_history (user_id, winner, points_earned, moves_count)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, winner, points_earned, moves_count),
                )
                conn.commit()
        except Exception:
            pass
