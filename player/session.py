"""Player session management (Guest & Authenticated User state)."""
from typing import Optional
from database.models import User
from database.repository import UserRepository


class SessionManager:
    """Tracks current active player, guest status, and session points."""

    def __init__(self, user_repo: Optional[UserRepository] = None):
        self.user_repo = user_repo or UserRepository()
        self.current_user: Optional[User] = None
        self.is_guest: bool = True
        self.guest_session_points: int = 0
        self.match_points_earned: int = 0

    def login_as_guest(self) -> None:
        """Switch to guest mode."""
        self.current_user = None
        self.is_guest = True

    def login_user(self, user: User) -> None:
        """Set current active logged-in user."""
        self.current_user = user
        self.is_guest = False

    def get_display_name(self) -> str:
        """Return username or Guest."""
        if self.is_guest or not self.current_user:
            return "Guest Player"
        return self.current_user.username

    def get_total_points(self) -> int:
        """Return total saved points for user or current session points for guest."""
        if self.is_guest or not self.current_user:
            return self.guest_session_points
        return self.current_user.points

    def award_match_points(self, points: int) -> int:
        """Add points from match to session and persist if logged in."""
        self.match_points_earned = points
        if self.is_guest or not self.current_user:
            self.guest_session_points += points
            return self.guest_session_points
        else:
            updated_total = self.user_repo.add_points(self.current_user.id, points)
            self.current_user.points = updated_total
            return updated_total

    def reset_session(self) -> None:
        """Reset match points tracking."""
        self.match_points_earned = 0
