"""Data models for PyChess database persistence."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a registered chess player account."""
    id: int
    username: str
    points: int = 0
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "User":
        """Create a User instance from a sqlite3 row/tuple."""
        return cls(
            id=row[0],
            username=row[1],
            points=row[2],
            created_at=str(row[3]) if len(row) > 3 and row[3] is not None else None,
        )
