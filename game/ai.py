"""AI engine for automated Black piece moves."""
import random
from typing import List, Optional, Tuple

from game.constants import BLACK
from game.rules import get_all_legal_moves_for_color


class ChessAI:
    """Computes and selects moves for Black chess pieces."""

    @staticmethod
    def get_best_move(board_matrix: List[List[str]]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Finds and returns a legal move for Black as ((from_row, from_col), (to_row, to_col))."""
        movable_pieces = get_all_legal_moves_for_color(board_matrix, BLACK)
        if not movable_pieces:
            return None

        # Prioritize captures if available
        capture_moves = []
        regular_moves = []

        for (from_r, from_c), moves in movable_pieces:
            for to_r, to_c in moves:
                target = board_matrix[to_r][to_c]
                if target.startswith("w"):
                    # Weight capture by target piece value (Queen > Rook > Bishop/Knight > Pawn)
                    weight = {"wq": 9, "wr": 5, "wb": 3, "wn": 3, "wp": 1}.get(target, 1)
                    capture_moves.append((weight, ((from_r, from_c), (to_r, to_c))))
                else:
                    regular_moves.append(((from_r, from_c), (to_r, to_c)))

        if capture_moves:
            # Sort by highest value capture first
            capture_moves.sort(key=lambda x: x[0], reverse=True)
            # Pick from highest value captures with slight randomization
            max_weight = capture_moves[0][0]
            best_captures = [move for weight, move in capture_moves if weight == max_weight]
            return random.choice(best_captures)

        if regular_moves:
            return random.choice(regular_moves)

        # Fallback
        origin, destinations = random.choice(movable_pieces)
        return (origin, random.choice(destinations))
