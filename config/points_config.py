"""Points configuration module for PyChess.

Defines point values awarded for captures, tactical plays, checks, and victories.
"""

POINTS = {
    # Piece captures
    "pawn_capture": 10,
    "knight_capture": 30,
    "bishop_capture": 30,
    "rook_capture": 50,
    "queen_capture": 90,

    # Strategic moves
    "pawn_promotion": 40,
    "check": 20,
    "checkmate": 100,

    # Game outcomes
    "win": 200,
    "loss": 0,
    "draw": 25,
}

# Mapping piece character codes to capture point event keys
PIECE_CAPTURE_MAP = {
    "p": "pawn_capture",
    "n": "knight_capture",
    "b": "bishop_capture",
    "r": "rook_capture",
    "q": "queen_capture",
}

# Human-readable labels and values for UI point explanation table
POINT_RULES_TABLE = [
    ("Capture Pawn", "+10 pts"),
    ("Capture Knight", "+30 pts"),
    ("Capture Bishop", "+30 pts"),
    ("Capture Rook", "+50 pts"),
    ("Capture Queen", "+90 pts"),
    ("Pawn Promotion", "+40 pts"),
    ("Deliver Check", "+20 pts"),
    ("Deliver Checkmate", "+100 pts"),
    ("Victory Bonus", "+200 pts"),
]
