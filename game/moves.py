"""Move generator for all chess pieces."""
from typing import List, Tuple
from game.constants import WHITE, BLACK


def get_pseudo_legal_moves(board_matrix: List[List[str]], row: int, col: int) -> List[Tuple[int, int]]:
    """Returns all pseudo-legal target squares for piece at (row, col)."""
    piece = board_matrix[row][col]
    if not piece:
        return []

    if piece == "wp":
        return moves_white_pawn(board_matrix, row, col)
    elif piece == "bp":
        return moves_black_pawn(board_matrix, row, col)
    elif piece == "wr":
        return moves_white_rook(board_matrix, row, col)
    elif piece == "br":
        return moves_black_rook(board_matrix, row, col)
    elif piece == "wn":
        return moves_white_knight(board_matrix, row, col)
    elif piece == "bn":
        return moves_black_knight(board_matrix, row, col)
    elif piece == "wb":
        return moves_white_bishop(board_matrix, row, col)
    elif piece == "bb":
        return moves_black_bishop(board_matrix, row, col)
    elif piece == "wq":
        return moves_white_queen(board_matrix, row, col)
    elif piece == "bq":
        return moves_black_queen(board_matrix, row, col)
    elif piece == "wk":
        return moves_white_king(board_matrix, row, col)
    elif piece == "bk":
        return moves_black_king(board_matrix, row, col)
    return []


def moves_white_pawn(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for white pawn (wp)."""
    moves = []
    # Move forward 1 if free
    if fila > 0 and tablero[fila - 1][columna] == "":
        moves.append((fila - 1, columna))
        # Move forward 2 if in starting row 6
        if fila == 6 and tablero[fila - 2][columna] == "":
            moves.append((fila - 2, columna))

    # Diagonal captures
    if fila > 0 and columna > 0 and tablero[fila - 1][columna - 1].startswith("b"):
        moves.append((fila - 1, columna - 1))
    if fila > 0 and columna < 7 and tablero[fila - 1][columna + 1].startswith("b"):
        moves.append((fila - 1, columna + 1))

    return moves


def moves_black_pawn(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for black pawn (bp)."""
    moves = []
    # Move forward 1 if free
    if fila < 7 and tablero[fila + 1][columna] == "":
        moves.append((fila + 1, columna))
        # Move forward 2 if in starting row 1
        if fila == 1 and tablero[fila + 2][columna] == "":
            moves.append((fila + 2, columna))

    # Diagonal captures
    if fila < 7 and columna < 7 and tablero[fila + 1][columna + 1].startswith("w"):
        moves.append((fila + 1, columna + 1))
    if fila < 7 and columna > 0 and tablero[fila + 1][columna - 1].startswith("w"):
        moves.append((fila + 1, columna - 1))

    return moves


def moves_white_rook(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for white rook (wr)."""
    moves = []
    # Up
    for i in range(fila - 1, -1, -1):
        if tablero[i][columna] == "":
            moves.append((i, columna))
        elif tablero[i][columna].startswith("b"):
            moves.append((i, columna))
            break
        else:
            break
    # Down
    for i in range(fila + 1, 8):
        if tablero[i][columna] == "":
            moves.append((i, columna))
        elif tablero[i][columna].startswith("b"):
            moves.append((i, columna))
            break
        else:
            break
    # Left
    for j in range(columna - 1, -1, -1):
        if tablero[fila][j] == "":
            moves.append((fila, j))
        elif tablero[fila][j].startswith("b"):
            moves.append((fila, j))
            break
        else:
            break
    # Right
    for j in range(columna + 1, 8):
        if tablero[fila][j] == "":
            moves.append((fila, j))
        elif tablero[fila][j].startswith("b"):
            moves.append((fila, j))
            break
        else:
            break
    return moves


def moves_black_rook(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for black rook (br)."""
    moves = []
    # Up
    for i in range(fila - 1, -1, -1):
        if tablero[i][columna] == "":
            moves.append((i, columna))
        elif tablero[i][columna].startswith("w"):
            moves.append((i, columna))
            break
        else:
            break
    # Down
    for i in range(fila + 1, 8):
        if tablero[i][columna] == "":
            moves.append((i, columna))
        elif tablero[i][columna].startswith("w"):
            moves.append((i, columna))
            break
        else:
            break
    # Left
    for j in range(columna - 1, -1, -1):
        if tablero[fila][j] == "":
            moves.append((fila, j))
        elif tablero[fila][j].startswith("w"):
            moves.append((fila, j))
            break
        else:
            break
    # Right
    for j in range(columna + 1, 8):
        if tablero[fila][j] == "":
            moves.append((fila, j))
        elif tablero[fila][j].startswith("w"):
            moves.append((fila, j))
            break
        else:
            break
    return moves


def moves_white_knight(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for white knight (wn)."""
    moves = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in deltas:
        nr, nc = fila + dr, columna + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = tablero[nr][nc]
            if target == "" or target.startswith("b"):
                moves.append((nr, nc))
    return moves


def moves_black_knight(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for black knight (bn)."""
    moves = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in deltas:
        nr, nc = fila + dr, columna + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = tablero[nr][nc]
            if target == "" or target.startswith("w"):
                moves.append((nr, nc))
    return moves


def moves_white_bishop(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for white bishop (wb)."""
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = fila + dr, columna + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target = tablero[nr][nc]
            if target == "":
                moves.append((nr, nc))
            elif target.startswith("b"):
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves


def moves_black_bishop(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for black bishop (bb)."""
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = fila + dr, columna + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target = tablero[nr][nc]
            if target == "":
                moves.append((nr, nc))
            elif target.startswith("w"):
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves


def moves_white_queen(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for white queen (wq)."""
    return moves_white_bishop(tablero, fila, columna) + moves_white_rook(tablero, fila, columna)


def moves_black_queen(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for black queen (bq)."""
    return moves_black_bishop(tablero, fila, columna) + moves_black_rook(tablero, fila, columna)


def moves_white_king(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for white king (wk)."""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = fila + dr, columna + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = tablero[nr][nc]
            if target == "" or target.startswith("b"):
                moves.append((nr, nc))
    return moves


def moves_black_king(tablero: List[List[str]], fila: int, columna: int) -> List[Tuple[int, int]]:
    """Valid moves for black king (bk)."""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = fila + dr, columna + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = tablero[nr][nc]
            if target == "" or target.startswith("w"):
                moves.append((nr, nc))
    return moves


def handle_pawn_promotion(tablero: List[List[str]], fila: int, columna: int) -> bool:
    """Promotes pawn to queen if it reaches the end rank. Returns True if promoted."""
    piece = tablero[fila][columna]
    if piece == "wp" and fila == 0:
        tablero[fila][columna] = "wq"
        return True
    elif piece == "bp" and fila == 7:
        tablero[fila][columna] = "bq"
        return True
    return False
