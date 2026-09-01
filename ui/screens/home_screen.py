"""Home screen / Main Menu interface."""
import pygame
from typing import TYPE_CHECKING

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, UI_COLORS
from ui.screens.base_screen import BaseScreen
from ui.components.button import Button
from ui.components.card import draw_panel, draw_badge
from ui.components.theme import get_font, load_piece_images

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class HomeScreen(BaseScreen):
    """Main menu providing entry to play, account, points, and settings."""

    def __init__(self, manager: "ScreenManager"):
        super().__init__(manager)
        self.buttons = []
        self._init_buttons()

    def _init_buttons(self) -> None:
        btn_w, btn_h = 280, 50
        start_x = (WINDOW_WIDTH - btn_w) // 2
        start_y = 230
        gap = 62

        self.buttons = [
            Button(
                (start_x, start_y, btn_w, btn_h),
                "Play Chess",
                on_click=lambda: self.manager.switch_to("game"),
                bg_color=UI_COLORS["accent_primary"],
                hover_color=UI_COLORS["accent_hover"],
            ),
            Button(
                (start_x, start_y + gap, btn_w, btn_h),
                "Player Account",
                on_click=lambda: self.manager.switch_to("account"),
                bg_color=UI_COLORS["accent_blue"],
                hover_color=UI_COLORS["accent_blue_hover"],
            ),
            Button(
                (start_x, start_y + gap * 2, btn_w, btn_h),
                "Points & Records",
                on_click=lambda: self.manager.switch_to("points"),
                bg_color=UI_COLORS["bg_card"],
                hover_color=(55, 62, 72),
            ),
            Button(
                (start_x, start_y + gap * 3, btn_w, btn_h),
                "Settings",
                on_click=lambda: self.manager.switch_to("settings"),
                bg_color=UI_COLORS["bg_card"],
                hover_color=(55, 62, 72),
            ),
            Button(
                (start_x, start_y + gap * 4, btn_w, btn_h),
                "Exit Game",
                on_click=self._exit_game,
                bg_color=(50, 25, 25),
                hover_color=UI_COLORS["accent_red_hover"],
            ),
        ]

    def _exit_game(self) -> None:
        self.manager.running = False

    def enter(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(UI_COLORS["bg_dark"])

        # Central decorative panel
        panel_w, panel_h = 420, 540
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = 40
        draw_panel(surface, (panel_x, panel_y, panel_w, panel_h))

        # Title
        title_font = get_font(42, bold=True)
        title_surf = title_font.render("PyChess", True, UI_COLORS["text_primary"])
        surface.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH // 2, 85)))

        subtitle_font = get_font(14)
        sub_surf = subtitle_font.render("Classic Chess with Progression & Points", True, UI_COLORS["text_secondary"])
        surface.blit(sub_surf, sub_surf.get_rect(center=(WINDOW_WIDTH // 2, 120)))

        # Player profile banner inside menu
        session = self.manager.session
        player_name = session.get_display_name()
        total_pts = session.get_total_points()

        badge_y = 150
        card_w = 340
        card_x = (WINDOW_WIDTH - card_w) // 2
        draw_panel(surface, (card_x, badge_y, card_w, 55), bg_color=UI_COLORS["bg_card"], border_radius=8)

        user_font = get_font(16, bold=True)
        u_surf = user_font.render(player_name, True, UI_COLORS["text_primary"])
        surface.blit(u_surf, (card_x + 16, badge_y + 10))

        pts_font = get_font(14)
        pts_label = f"Session Points: {total_pts}" if session.is_guest else f"Total Points: {total_pts:,}"
        p_surf = pts_font.render(pts_label, True, UI_COLORS["accent_gold"])
        surface.blit(p_surf, (card_x + 16, badge_y + 30))

        status_text = "GUEST" if session.is_guest else "ACCOUNT"
        status_color = UI_COLORS["text_secondary"] if session.is_guest else UI_COLORS["accent_primary"]
        draw_badge(surface, (card_x + card_w - 95, badge_y + 14, 80, 26), status_text, text_color=status_color)

        # Draw buttons
        for btn in self.buttons:
            btn.draw(surface)
