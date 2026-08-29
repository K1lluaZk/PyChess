"""Game state controller coordinating board, turns, moves, rules, and points."""
from enum import Enum
from typing import List, Optional, Tuple

from game.board import Board
from game.constants import WHITE, BLACK
from game.moves import handle_pawn_promotion
from game.rules import (
    get_legal_moves,
    is_in_check,
    is_checkmate,
    is_stalemate,
)
from game.ai import ChessAI
from game.points_engine import PointsEngine


class GameStatus(Enum):
    IN_PROGRESS = "in_progress"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"


class GameState:
    """Manages the full lifecycle and state transitions of a chess match."""

    def __init__(self):
        self.board = Board()
        self.points_engine = PointsEngine()
        self.turn: str = WHITE
        self.selected_square: Optional[Tuple[int, int]] = None
        self.valid_moves: List[Tuple[int, int]] = []
        self.last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.status: GameStatus = GameStatus.IN_PROGRESS
        self.winner: Optional[str] = None
        self.moves_count: int = 0
        self.captured_by_white: List[str] = []
        self.captured_by_black: List[str] = []

    def reset(self) -> None:
        """Reset the match to initial board and zero points."""
        self.board.reset()
        self.points_engine.reset()
        self.turn = WHITE
        self.selected_square = None
        self.valid_moves.clear()
        self.last_move = None
        self.status = GameStatus.IN_PROGRESS
        self.winner = None
        self.moves_count = 0
        self.captured_by_white.clear()
        self.captured_by_black.clear()

    def handle_square_click(self, row: int, col: int) -> bool:
        """Handles player interaction on clicking square (row, col). Returns True if a move was executed."""
        if self.status in (GameStatus.CHECKMATE, GameStatus.STALEMATE):
            return False

        # If White player already has a selected piece and clicks a valid destination square
        if self.selected_square:
            if (row, col) in self.valid_moves:
                from_row, from_col = self.selected_square
                self._execute_player_move((from_row, from_col), (row, col))
                self.selected_square = None
                self.valid_moves.clear()
                return True

            # If clicking own white piece again, re-select
            piece = self.board.get_piece(row, col)
            if piece.startswith(WHITE):
                self.selected_square = (row, col)
                self.valid_moves = get_legal_moves(self.board.grid, row, col)
                return False

            # Deselect if clicking elsewhere
            self.selected_square = None
            self.valid_moves.clear()
            return False

        # If no piece is selected yet, check if clicking a movable piece
        piece = self.board.get_piece(row, col)
        if piece and piece.startswith(self.turn):
            self.selected_square = (row, col)
            self.valid_moves = get_legal_moves(self.board.grid, row, col)

        return False

    def _execute_player_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        """Executes a move for White, updates points, and triggers AI turn."""
        from_r, from_c = from_pos
        to_r, to_c = to_pos
        piece = self.board.get_piece(from_r, from_c)
        captured = self.board.move_piece(from_pos, to_pos)

        self.last_move = (from_pos, to_pos)
        self.moves_count += 1

        # Point rewards for capture
        if captured:
            self.captured_by_white.append(captured)
            self.points_engine.on_piece_captured(captured)

        # Pawn promotion
        if handle_pawn_promotion(self.board.grid, to_r, to_c):
            self.points_engine.on_pawn_promoted()

        # Check if Black is in checkmate
        if is_checkmate(self.board.grid, BLACK):
            self.status = GameStatus.CHECKMATE
            self.winner = "White"
            self.points_engine.on_checkmate_delivered()
            self.points_engine.on_game_won()
            return
        elif is_stalemate(self.board.grid, BLACK):
            self.status = GameStatus.STALEMATE
            self.winner = None
            return
        elif is_in_check(self.board.grid, BLACK):
            self.status = GameStatus.CHECK
            self.points_engine.on_check_delivered()
        else:
            self.status = GameStatus.IN_PROGRESS

        # Switch to Black turn & execute AI move
        self.turn = BLACK
        self.execute_ai_turn()

    def execute_ai_turn(self) -> None:
        """Computes and executes AI move for Black."""
        if self.status in (GameStatus.CHECKMATE, GameStatus.STALEMATE):
            return

        ai_move = ChessAI.get_best_move(self.board.grid)
        if not ai_move:
            # No legal moves for Black
            if is_in_check(self.board.grid, BLACK):
                self.status = GameStatus.CHECKMATE
                self.winner = "White"
                self.points_engine.on_checkmate_delivered()
                self.points_engine.on_game_won()
            else:
                self.status = GameStatus.STALEMATE
            return

        origin, destination = ai_move
        from_r, from_c = origin
        to_r, to_c = destination
        captured = self.board.move_piece(origin, destination)
        self.last_move = (origin, destination)
        self.moves_count += 1

        if captured:
            self.captured_by_black.append(captured)

        # Black pawn promotion
        handle_pawn_promotion(self.board.grid, to_r, to_c)

        # Check if White is in checkmate or check
        if is_checkmate(self.board.grid, WHITE):
            self.status = GameStatus.CHECKMATE
            self.winner = "Black"
        elif is_stalemate(self.board.grid, WHITE):
            self.status = GameStatus.STALEMATE
        elif is_in_check(self.board.grid, WHITE):
            self.status = GameStatus.CHECK
        else:
            self.status = GameStatus.IN_PROGRESS

        self.turn = WHITE
