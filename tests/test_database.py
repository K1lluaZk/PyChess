"""Unit tests for SQLite database, repository, and session manager."""
import os
import tempfile
import unittest

from database.db import Database
from database.repository import UserRepository
from player.session import SessionManager


class TestDatabaseAndSession(unittest.TestCase):

    def setUp(self):
        # Create temporary database file
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db = Database(db_path=self.temp_file.name)
        self.user_repo = UserRepository(self.db)
        self.session = SessionManager(self.user_repo)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_create_and_get_user(self):
        user = self.user_repo.create_user("Mario", initial_points=100)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "Mario")
        self.assertEqual(user.points, 100)

        fetched = self.user_repo.get_user_by_username("mario")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, user.id)
        self.assertEqual(fetched.points, 100)

    def test_duplicate_username_returns_none(self):
        user1 = self.user_repo.create_user("Luigi")
        self.assertIsNotNone(user1)

        user2 = self.user_repo.create_user("luigi")
        self.assertIsNone(user2)

    def test_add_points(self):
        user = self.user_repo.create_user("Peach", initial_points=50)
        new_total = self.user_repo.add_points(user.id, 120)
        self.assertEqual(new_total, 170)

        updated = self.user_repo.get_user_by_id(user.id)
        self.assertEqual(updated.points, 170)

    def test_top_players(self):
        self.user_repo.create_user("Player1", initial_points=100)
        self.user_repo.create_user("Player2", initial_points=500)
        self.user_repo.create_user("Player3", initial_points=300)

        top = self.user_repo.get_top_players(limit=2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].username, "Player2")
        self.assertEqual(top[1].username, "Player3")

    def test_guest_session_flow(self):
        self.assertTrue(self.session.is_guest)
        self.assertEqual(self.session.get_display_name(), "Guest Player")
        self.assertEqual(self.session.get_total_points(), 0)

        self.session.award_match_points(150)
        self.assertEqual(self.session.get_total_points(), 150)
        self.assertTrue(self.session.is_guest)

    def test_logged_in_user_session_flow(self):
        user = self.user_repo.create_user("Yoshi", initial_points=200)
        self.session.login_user(user)

        self.assertFalse(self.session.is_guest)
        self.assertEqual(self.session.get_display_name(), "Yoshi")
        self.assertEqual(self.session.get_total_points(), 200)

        self.session.award_match_points(180)
        self.assertEqual(self.session.get_total_points(), 380)

        # Verify DB persistence
        db_user = self.user_repo.get_user_by_id(user.id)
        self.assertEqual(db_user.points, 380)


if __name__ == "__main__":
    unittest.main()
