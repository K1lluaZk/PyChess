"""Chessboard data representation and state manipulation."""
import copy
from typing import List, Optional, Tuple

from game.constants import INITIAL_BOARD_LAYOUT, WHITE_KING, BLACK_KING, WHITE


class Board:
    """Represents the 8x8 chess board matrix and provides board operations."""

    def __init__(self, grid: Optional[List[List[str]]] = None):
        if grid is not None:
            self.grid = [row[:] for row in grid]
        else:
            self.reset()

    def reset(self) -> None:
        """Reset the board to the standard starting chess position."""
        self.grid = [row[:] for row in INITIAL_BOARD_LAYOUT]

    def get_piece(self, row: int, col: int) -> str:
        """Get the piece string at the specified square."""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return ""

    def set_piece(self, row: int, col: int, piece: str) -> None:
        """Set the piece at the specified square."""
        if 0 <= row < 8 and 0 <= col < 8:
            self.grid[row][col] = piece

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> str:
        """Move piece from source to destination. Returns captured piece string (if any)."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.grid[from_row][from_col]
        captured = self.grid[to_row][to_col]
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = ""
        return captured

    def find_king(self, color: str) -> Optional[Tuple[int, int]]:
        """Find row and col position of king for given color ('w' or 'b')."""
        target_king = WHITE_KING if color == WHITE else BLACK_KING
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] == target_king:
                    return (row, col)
        return None

    def clone(self) -> "Board":
        """Return a deep copy of the current board."""
        return Board([row[:] for row in self.grid])

    def to_matrix(self) -> List[List[str]]:
        """Return a copy of the raw 8x8 matrix."""
        return [row[:] for row in self.grid]
