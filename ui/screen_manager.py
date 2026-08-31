"""Screen manager managing state machine and navigation transitions."""
import pygame
from typing import Any, Dict, Optional

from config.settings import DEFAULT_SETTINGS
from database.repository import UserRepository
from player.session import SessionManager
from ui.screens.base_screen import BaseScreen
from ui.screens.home_screen import HomeScreen
from ui.screens.account_screen import AccountScreen
from ui.screens.game_screen import GameScreen
from ui.screens.points_screen import PointsScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.result_screen import ResultScreen


class ScreenManager:
    """Manages active screens, transitions, and shared game context."""

    def __init__(self, user_repo: Optional[UserRepository] = None, session: Optional[SessionManager] = None):
        self.user_repo = user_repo or UserRepository()
        self.session = session or SessionManager(self.user_repo)
        self.settings: Dict[str, Any] = dict(DEFAULT_SETTINGS)
        self.running: bool = True

        # Initialize all screen instances
        self.screens: Dict[str, BaseScreen] = {
            "home": HomeScreen(self),
            "account": AccountScreen(self),
            "game": GameScreen(self),
            "points": PointsScreen(self),
            "settings": SettingsScreen(self),
            "result": ResultScreen(self),
        }
        self.active_screen_name: str = "home"
        self.active_screen: BaseScreen = self.screens["home"]

    def switch_to(self, screen_name: str, **kwargs) -> None:
        """Transitions to target screen with optional context parameters."""
        if screen_name in self.screens:
            self.active_screen_name = screen_name
            self.active_screen = self.screens[screen_name]

            # Special parameter injection for result screen
            if screen_name == "result" and isinstance(self.active_screen, ResultScreen):
                self.active_screen.set_result(
                    winner=kwargs.get("winner"),
                    points=kwargs.get("points", 0),
                    events=kwargs.get("events", []),
                    moves=kwargs.get("moves", 0),
                )

            self.active_screen.enter()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Delegates event to the current active screen."""
        if event.type == pygame.QUIT:
            self.running = False
            return
        self.active_screen.handle_event(event)

    def update(self) -> None:
        """Delegates frame update to the active screen."""
        self.active_screen.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Delegates render pass to the active screen."""
        self.active_screen.draw(surface)
