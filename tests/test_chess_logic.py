"""Unit tests for chess board, moves, rules, and points engine."""
import unittest

from game.constants import WHITE, BLACK
from game.board import Board
from game.moves import (
    moves_white_pawn,
    moves_black_pawn,
    moves_white_knight,
    moves_white_bishop,
    moves_white_rook,
    moves_white_queen,
    moves_white_king,
    handle_pawn_promotion,
)
from game.rules import (
    is_in_check,
    is_checkmate,
    is_stalemate,
    get_legal_moves,
)
from game.points_engine import PointsEngine


class TestChessLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_setup(self):
        self.assertEqual(self.board.get_piece(0, 0), "br")
        self.assertEqual(self.board.get_piece(7, 4), "wk")
        self.assertEqual(self.board.get_piece(6, 0), "wp")
        self.assertEqual(self.board.get_piece(3, 3), "")

    def test_pawn_moves_initial(self):
        # White pawn at row 6, col 4 has 2 forward moves
        moves = moves_white_pawn(self.board.grid, 6, 4)
        self.assertIn((5, 4), moves)
        self.assertIn((4, 4), moves)
        self.assertEqual(len(moves), 2)

    def test_knight_moves(self):
        # White knight at (7, 1) has 2 initial moves (5, 0) and (5, 2)
        moves = moves_white_knight(self.board.grid, 7, 1)
        self.assertIn((5, 0), moves)
        self.assertIn((5, 2), moves)
        self.assertEqual(len(moves), 2)

    def test_pawn_promotion(self):
        # Place pawn on row 0
        board = [["" for _ in range(8)] for _ in range(8)]
        board[0][3] = "wp"
        promoted = handle_pawn_promotion(board, 0, 3)
        self.assertTrue(promoted)
        self.assertEqual(board[0][3], "wq")

    def test_check_detection(self):
        board = [["" for _ in range(8)] for _ in range(8)]
        board[7][4] = "wk"  # White king at e1
        board[0][4] = "br"  # Black rook attacking on e-file
        self.assertTrue(is_in_check(board, WHITE))

        # Block with white pawn at e2
        board[6][4] = "wp"
        self.assertFalse(is_in_check(board, WHITE))

    def test_back_rank_checkmate(self):
        # Back-rank mate: Black King trapped at (0, 7) by own pawns at (1, 6), (1, 7), (1, 5)
        # and attacked along rank 0 by White Queen at (0, 0)
        board = [["" for _ in range(8)] for _ in range(8)]
        board[0][7] = "bk"  # Black king on h8
        board[1][7] = "bp"  # Black pawn on h7
        board[1][6] = "bp"  # Black pawn on g7
        board[1][5] = "bp"  # Black pawn on f7
        board[0][0] = "wq"  # White queen delivers check on rank 0
        board[7][4] = "wk"  # White king

        self.assertTrue(is_in_check(board, BLACK))
        self.assertTrue(is_checkmate(board, BLACK))

    def test_stalemate_detection(self):
        # King on corner (0, 0) with no legal moves but not in check
        board = [["" for _ in range(8)] for _ in range(8)]
        board[0][0] = "bk"  # Black king on a8
        board[1][2] = "wq"  # White queen on c7 (covers (0, 1), (1, 0), (1, 1), but NOT (0, 0))
        board[2][1] = "wk"  # White king on b6 (protects queen)

        self.assertFalse(is_in_check(board, BLACK))
        self.assertTrue(is_stalemate(board, BLACK))

    def test_points_engine(self):
        engine = PointsEngine()
        self.assertEqual(engine.total_points, 0)

        pts = engine.on_piece_captured("bp")
        self.assertEqual(pts, 10)
        self.assertEqual(engine.total_points, 10)

        pts_q = engine.on_piece_captured("bq")
        self.assertEqual(pts_q, 90)
        self.assertEqual(engine.total_points, 100)

        pts_chk = engine.on_check_delivered()
        self.assertEqual(pts_chk, 20)

        pts_mate = engine.on_checkmate_delivered()
        self.assertEqual(pts_mate, 100)

        pts_win = engine.on_game_won()
        self.assertEqual(pts_win, 200)

        self.assertEqual(engine.total_points, 420)
        self.assertEqual(len(engine.get_breakdown()), 5)


if __name__ == "__main__":
    unittest.main()
