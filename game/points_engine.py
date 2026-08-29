"""Points Engine: calculates points awarded during chess match events."""
from typing import Dict, List, Optional
from config.points_config import POINTS, PIECE_CAPTURE_MAP


class PointsEvent:
    """Represents a single point-earning event in the game."""

    def __init__(self, description: str, points: int):
        self.description = description
        self.points = points


class PointsEngine:
    """Tracks and calculates points accumulated throughout a single chess game."""

    def __init__(self, point_config: Optional[Dict[str, int]] = None):
        self.config = point_config or POINTS
        self.total_points: int = 0
        self.events: List[PointsEvent] = []

    def reset(self) -> None:
        """Reset match points tracking for a new game."""
        self.total_points = 0
        self.events.clear()

    def record_event(self, event_key: str, custom_description: Optional[str] = None) -> int:
        """Record a point event by key from configuration and return points awarded."""
        pts = self.config.get(event_key, 0)
        desc = custom_description or event_key.replace("_", " ").title()
        self.total_points += pts
        self.events.append(PointsEvent(desc, pts))
        return pts

    def on_piece_captured(self, captured_piece: str) -> int:
        """Evaluate points for capturing an opponent piece (e.g. 'bp', 'br', 'bn', 'bb', 'bq')."""
        if not captured_piece or len(captured_piece) < 2:
            return 0

        piece_type = captured_piece[1]  # 'p', 'n', 'b', 'r', 'q', 'k'
        event_key = PIECE_CAPTURE_MAP.get(piece_type)
        if event_key:
            piece_name = {
                "p": "Pawn", "n": "Knight", "b": "Bishop", "r": "Rook", "q": "Queen"
            }.get(piece_type, "Piece")
            return self.record_event(event_key, f"Captured Black {piece_name}")
        return 0

    def on_pawn_promoted(self) -> int:
        """Evaluate points for advancing a pawn to queen."""
        return self.record_event("pawn_promotion", "Pawn Promoted to Queen")

    def on_check_delivered(self) -> int:
        """Evaluate points for delivering a check to opponent king."""
        return self.record_event("check", "Delivered Check")

    def on_checkmate_delivered(self) -> int:
        """Evaluate points for delivering checkmate."""
        return self.record_event("checkmate", "Delivered Checkmate")

    def on_game_won(self) -> int:
        """Evaluate points for winning the chess match."""
        return self.record_event("win", "Victory Bonus")

    def get_breakdown(self) -> List[PointsEvent]:
        """Return all point events recorded during this match."""
        return list(self.events)
