"""Main entry point for PyChess application."""
import sys
import pygame

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from database.db import Database
from database.repository import UserRepository
from player.session import SessionManager
from ui.screen_manager import ScreenManager


def main() -> None:
    """Initializes Pygame display, managers, and starts the game loop."""
    pygame.init()
    pygame.font.init()

    # Create display window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyChess - Python Chess Game")
    clock = pygame.time.Clock()

    # Initialize data layer and session
    db = Database()
    user_repo = UserRepository(db)
    session = SessionManager(user_repo)

    # Initialize screen coordinator
    screen_manager = ScreenManager(user_repo=user_repo, session=session)

    # Main application loop
    while screen_manager.running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            screen_manager.handle_event(event)

        # State updates
        screen_manager.update()

        # Render pass
        screen_manager.draw(window)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
