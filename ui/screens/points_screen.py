"""Points and scoring breakdown screen."""
import pygame
from typing import List, TYPE_CHECKING

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, UI_COLORS
from config.points_config import POINT_RULES_TABLE
from database.models import User
from ui.screens.base_screen import BaseScreen
from ui.components.button import Button
from ui.components.card import draw_panel, draw_badge
from ui.components.theme import get_font

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class PointsScreen(BaseScreen):
    """Displays player points, point rewards reference, and database leaderboard."""

    def __init__(self, manager: "ScreenManager"):
        super().__init__(manager)
        self.top_players: List[User] = []
        center_x = WINDOW_WIDTH // 2
        self.back_btn = Button(
            (center_x - 120, 540, 240, 44),
            "Back to Menu",
            on_click=lambda: self.manager.switch_to("home"),
            bg_color=UI_COLORS["bg_card"],
            hover_color=(55, 62, 72),
            font_size=16,
        )

    def enter(self) -> None:
        self.top_players = self.manager.user_repo.get_top_players(limit=6)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.back_btn.handle_event(event)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.back_btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(UI_COLORS["bg_dark"])

        # Main header
        title_font = get_font(28, bold=True)
        title_surf = title_font.render("Points & Leaderboard", True, UI_COLORS["text_primary"])
        surface.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH // 2, 40)))

        # Top Player Profile Card
        session = self.manager.session
        panel_w = 760
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        draw_panel(surface, (panel_x, 70, panel_w, 80), bg_color=UI_COLORS["bg_panel"])

        name_font = get_font(18, bold=True)
        p_name = session.get_display_name()
        n_surf = name_font.render(p_name, True, UI_COLORS["text_primary"])
        surface.blit(n_surf, (panel_x + 25, 85))

        status_text = "GUEST" if session.is_guest else "REGISTERED ACCOUNT"
        status_color = UI_COLORS["text_secondary"] if session.is_guest else UI_COLORS["accent_primary"]
        draw_badge(surface, (panel_x + 25, 115, 160, 22), status_text, text_color=status_color, font_size=11)

        # Points large display on right of profile card
        pts_font = get_font(24, bold=True)
        tot_pts = session.get_total_points()
        val_surf = pts_font.render(f"{tot_pts:,} PTS", True, UI_COLORS["accent_gold"])
        surface.blit(val_surf, (panel_x + panel_w - 200, 85))

        sub_pts_font = get_font(12)
        sub_label = "Guest points will not be permanently saved." if session.is_guest else "Saved to SQLite Database."
        sub_surf = sub_pts_font.render(sub_label, True, UI_COLORS["text_secondary"])
        surface.blit(sub_surf, (panel_x + panel_w - 280, 120))

        # Left Column: Points Scoring Guide Table
        col_w = 365
        draw_panel(surface, (panel_x, 165, col_w, 355), bg_color=UI_COLORS["bg_panel"])

        tbl_title_font = get_font(16, bold=True)
        t_surf = tbl_title_font.render("Points System Rules", True, UI_COLORS["text_primary"])
        surface.blit(t_surf, (panel_x + 20, 180))

        row_y = 215
        for action, reward in POINT_RULES_TABLE:
            row_font = get_font(13)
            a_surf = row_font.render(action, True, UI_COLORS["text_secondary"])
            r_surf = row_font.render(reward, True, UI_COLORS["accent_gold"])
            surface.blit(a_surf, (panel_x + 20, row_y))
            surface.blit(r_surf, (panel_x + col_w - 70, row_y))
            row_y += 33

        # Right Column: Leaderboard
        right_x = panel_x + col_w + 30
        draw_panel(surface, (right_x, 165, col_w, 355), bg_color=UI_COLORS["bg_panel"])

        lb_title = tbl_title_font.render("Top Players (SQLite DB)", True, UI_COLORS["text_primary"])
        surface.blit(lb_title, (right_x + 20, 180))

        if not self.top_players:
            none_font = get_font(13)
            no_surf = none_font.render("No registered player records yet.", True, UI_COLORS["text_secondary"])
            surface.blit(no_surf, (right_x + 20, 230))
        else:
            lb_y = 220
            for idx, user in enumerate(self.top_players):
                rank_color = UI_COLORS["accent_gold"] if idx == 0 else UI_COLORS["text_primary"]
                draw_panel(surface, (right_x + 15, lb_y, col_w - 30, 42), bg_color=UI_COLORS["bg_card"], border_radius=6)

                r_font = get_font(14, bold=True)
                rank_surf = r_font.render(f"#{idx + 1}", True, rank_color)
                surface.blit(rank_surf, (right_x + 28, lb_y + 12))

                u_name_surf = r_font.render(user.username, True, UI_COLORS["text_primary"])
                surface.blit(u_name_surf, (right_x + 65, lb_y + 12))

                p_surf = r_font.render(f"{user.points:,} pts", True, UI_COLORS["accent_gold"])
                surface.blit(p_surf, (right_x + col_w - 115, lb_y + 12))

                lb_y += 50

        # Back button
        self.back_btn.draw(surface)
