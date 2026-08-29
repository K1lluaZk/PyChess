"""Constants for chess pieces, colors, and board representations."""

# Player Colors
WHITE = "w"
BLACK = "b"

# Piece Types
PAWN = "p"
ROOK = "r"
KNIGHT = "n"
BISHOP = "b"
QUEEN = "q"
KING = "k"

# Piece Codes
WHITE_PAWN = "wp"
WHITE_ROOK = "wr"
WHITE_KNIGHT = "wn"
WHITE_BISHOP = "wb"
WHITE_QUEEN = "wq"
WHITE_KING = "wk"

BLACK_PAWN = "bp"
BLACK_ROOK = "br"
BLACK_KNIGHT = "bn"
BLACK_BISHOP = "bb"
BLACK_QUEEN = "bq"
BLACK_KING = "bk"

ALL_PIECES = [
    WHITE_PAWN, WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING,
    BLACK_PAWN, BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING,
]

# Initial Board State
INITIAL_BOARD_LAYOUT = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]
