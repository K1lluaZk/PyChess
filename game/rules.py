"""Chess rules validation: check, checkmate, stalemate, and legal move filtering."""
import copy
from typing import List, Optional, Tuple

from game.constants import WHITE, BLACK, WHITE_KING, BLACK_KING
from game.moves import get_pseudo_legal_moves


def is_in_check(board_matrix: List[List[str]], color: str) -> bool:
    """Check if the king of the given color ('w' or 'b') is in check."""
    target_king = WHITE_KING if color == WHITE else BLACK_KING
    enemy_prefix = BLACK if color == WHITE else WHITE

    king_pos: Optional[Tuple[int, int]] = None
    for row in range(8):
        for col in range(8):
            if board_matrix[row][col] == target_king:
                king_pos = (row, col)
                break
        if king_pos:
            break

    # If king is missing from board, treat as check/captured
    if king_pos is None:
        return True

    # Scan all enemy pieces to see if any attack the king's square
    for r in range(8):
        for c in range(8):
            piece = board_matrix[r][c]
            if piece.startswith(enemy_prefix):
                moves = get_pseudo_legal_moves(board_matrix, r, c)
                if king_pos in moves:
                    return True

    return False


def get_legal_moves(board_matrix: List[List[str]], row: int, col: int) -> List[Tuple[int, int]]:
    """Returns strictly legal moves for piece at (row, col) that do not leave own king in check."""
    piece = board_matrix[row][col]
    if not piece:
        return []

    color = WHITE if piece.startswith("w") else BLACK
    pseudo_moves = get_pseudo_legal_moves(board_matrix, row, col)
    legal_moves = []

    for dest_r, dest_c in pseudo_moves:
        # Simulate move on copy
        temp_board = [r[:] for r in board_matrix]
        temp_board[dest_r][dest_c] = piece
        temp_board[row][col] = ""

        # Only allow move if own king is not in check
        if not is_in_check(temp_board, color):
            legal_moves.append((dest_r, dest_c))

    return legal_moves


def get_all_legal_moves_for_color(board_matrix: List[List[str]], color: str) -> List[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
    """Returns list of ((from_row, from_col), [valid_destinations]) for all pieces of `color`."""
    prefix = WHITE if color == WHITE else BLACK
    moves_by_piece = []
    for r in range(8):
        for c in range(8):
            piece = board_matrix[r][c]
            if piece.startswith(prefix):
                moves = get_legal_moves(board_matrix, r, c)
                if moves:
                    moves_by_piece.append(((r, c), moves))
    return moves_by_piece


def has_legal_moves(board_matrix: List[List[str]], color: str) -> bool:
    """Returns True if player of given color has at least one legal move."""
    prefix = WHITE if color == WHITE else BLACK
    for r in range(8):
        for c in range(8):
            piece = board_matrix[r][c]
            if piece.startswith(prefix):
                if get_legal_moves(board_matrix, r, c):
                    return True
    return False


def is_checkmate(board_matrix: List[List[str]], color: str) -> bool:
    """Returns True if player of given color is in checkmate."""
    return is_in_check(board_matrix, color) and not has_legal_moves(board_matrix, color)


def is_stalemate(board_matrix: List[List[str]], color: str) -> bool:
    """Returns True if player of given color has no legal moves and is not in check."""
    return (not is_in_check(board_matrix, color)) and (not has_legal_moves(board_matrix, color))


def verify_winner(board_matrix: List[List[str]]) -> Optional[str]:
    """Check if a king has been captured or checkmated."""
    white_has_king = any(piece == WHITE_KING for row in board_matrix for piece in row)
    black_has_king = any(piece == BLACK_KING for row in board_matrix for piece in row)

    if not white_has_king:
        return "Black"
    if not black_has_king:
        return "White"

    if is_checkmate(board_matrix, BLACK):
        return "White"
    if is_checkmate(board_matrix, WHITE):
        return "Black"

    return None
