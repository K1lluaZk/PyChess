"""Base class interface for all UI screens."""
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class BaseScreen:
    """Abstract base class for all game screens."""

    def __init__(self, manager: "ScreenManager"):
        self.manager = manager

    def enter(self) -> None:
        """Called whenever this screen becomes the active screen."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process incoming Pygame events."""
        pass

    def update(self) -> None:
        """Update animations, timers, and component states."""
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Draw screen elements to the target surface."""
        pass
