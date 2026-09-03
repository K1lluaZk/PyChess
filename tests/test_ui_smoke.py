"""Smoke test for Pygame UI initialization and screen navigation."""
import os
import unittest
import pygame

# Set SDL to dummy video driver for headless testing
os.environ["SDL_VIDEODRIVER"] = "dummy"

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from database.db import Database
from database.repository import UserRepository
from player.session import SessionManager
from ui.screen_manager import ScreenManager
from ui.screens.home_screen import HomeScreen
from ui.screens.account_screen import AccountScreen
from ui.screens.game_screen import GameScreen
from ui.screens.points_screen import PointsScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.result_screen import ResultScreen


class TestUISmoke(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        cls.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.db = Database(db_path=":memory:")
        self.user_repo = UserRepository(self.db)
        self.session = SessionManager(self.user_repo)
        self.screen_manager = ScreenManager(user_repo=self.user_repo, session=self.session)

    def test_screen_transitions_and_draw(self):
        screens_to_test = ["home", "account", "game", "points", "settings", "result"]

        for name in screens_to_test:
            self.screen_manager.switch_to(name, winner="White", points=300, events=[], moves=12)
            self.assertEqual(self.screen_manager.active_screen_name, name)

            # Update & Draw pass
            self.screen_manager.update()
            self.screen_manager.draw(self.window)

    def test_game_click_and_piece_selection(self):
        self.screen_manager.switch_to("game")
        game_screen: GameScreen = self.screen_manager.active_screen

        # Simulate clicking on white pawn at row 6, col 4 (e2)
        game_screen.game_state.handle_square_click(6, 4)
        self.assertEqual(game_screen.game_state.selected_square, (6, 4))
        self.assertGreater(len(game_screen.game_state.valid_moves), 0)

        # Move to (4, 4) (e4)
        moved = game_screen.game_state.handle_square_click(4, 4)
        self.assertTrue(moved)
        self.assertEqual(game_screen.game_state.board.get_piece(4, 4), "wp")
        self.assertEqual(game_screen.game_state.board.get_piece(6, 4), "")


if __name__ == "__main__":
    unittest.main()
