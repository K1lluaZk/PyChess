"""Post-game victory, loss, or stalemate result screen."""
import pygame
from typing import List, Optional, TYPE_CHECKING

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, UI_COLORS
from game.points_engine import PointsEvent
from ui.screens.base_screen import BaseScreen
from ui.components.button import Button
from ui.components.card import draw_panel, draw_badge
from ui.components.theme import get_font

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class ResultScreen(BaseScreen):
    """Displays match results, points gained breakdown, and navigation buttons."""

    def __init__(self, manager: "ScreenManager"):
        super().__init__(manager)
        self.winner: Optional[str] = None
        self.points_earned: int = 0
        self.events: List[PointsEvent] = []
        self.moves_count: int = 0

        center_x = WINDOW_WIDTH // 2
        self.play_again_btn = Button(
            (center_x - 170, 450, 340, 46),
            "Play Again",
            on_click=lambda: self.manager.switch_to("game"),
            bg_color=UI_COLORS["accent_primary"],
            hover_color=UI_COLORS["accent_hover"],
            font_size=16,
        )

        self.menu_btn = Button(
            (center_x - 170, 510, 340, 46),
            "Main Menu",
            on_click=lambda: self.manager.switch_to("home"),
            bg_color=UI_COLORS["bg_card"],
            hover_color=(55, 62, 72),
            font_size=16,
        )

    def set_result(self, winner: Optional[str], points: int, events: List[PointsEvent], moves: int) -> None:
        """Configures result screen data for the completed match."""
        self.winner = winner
        self.points_earned = points
        self.events = events
        self.moves_count = moves

    def handle_event(self, event: pygame.event.Event) -> None:
        self.play_again_btn.handle_event(event)
        self.menu_btn.handle_event(event)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.play_again_btn.update(mouse_pos)
        self.menu_btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(UI_COLORS["bg_dark"])

        panel_w, panel_h = 460, 540
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = 35
        draw_panel(surface, (panel_x, panel_y, panel_w, panel_h))

        # Result Title & Subheading
        title_font = get_font(34, bold=True)
        if self.winner == "White":
            title_text = "VICTORY!"
            title_color = UI_COLORS["accent_primary"]
            sub_text = "Checkmate! White is victorious."
        elif self.winner == "Black":
            title_text = "DEFEAT"
            title_color = UI_COLORS["accent_red"]
            sub_text = "Checkmate! Black wins the match."
        else:
            title_text = "DRAW"
            title_color = UI_COLORS["accent_gold"]
            sub_text = "Stalemate! The match is a tie."

        t_surf = title_font.render(title_text, True, title_color)
        surface.blit(t_surf, t_surf.get_rect(center=(WINDOW_WIDTH // 2, 75)))

        sub_font = get_font(15)
        s_surf = sub_font.render(sub_text, True, UI_COLORS["text_secondary"])
        surface.blit(s_surf, s_surf.get_rect(center=(WINDOW_WIDTH // 2, 115)))

        # Points Card
        score_rect = (panel_x + 30, 140, panel_w - 60, 70)
        draw_panel(surface, score_rect, bg_color=UI_COLORS["bg_card"], border_radius=8)

        pts_label_font = get_font(13)
        pl_surf = pts_label_font.render("Points Earned This Match:", True, UI_COLORS["text_secondary"])
        surface.blit(pl_surf, (panel_x + 45, 152))

        pts_val_font = get_font(26, bold=True)
        pv_surf = pts_val_font.render(f"+{self.points_earned} PTS", True, UI_COLORS["accent_gold"])
        surface.blit(pv_surf, (panel_x + 45, 172))

        moves_font = get_font(14)
        m_surf = moves_font.render(f"Moves: {self.moves_count}", True, UI_COLORS["text_secondary"])
        surface.blit(m_surf, (panel_x + panel_w - 130, 165))

        # Points Breakdown List
        bd_title_font = get_font(14, bold=True)
        bd_surf = bd_title_font.render("Match Rewards Breakdown:", True, UI_COLORS["text_secondary"])
        surface.blit(bd_surf, (panel_x + 35, 230))

        start_y = 260
        if not self.events:
            empty_font = get_font(13)
            e_surf = empty_font.render("No points scored during this game.", True, (100, 110, 120))
            surface.blit(e_surf, (panel_x + 35, start_y))
        else:
            # Show last 5 events
            for i, ev in enumerate(self.events[-6:]):
                ev_font = get_font(13)
                desc_surf = ev_font.render(ev.description, True, UI_COLORS["text_primary"])
                val_surf = ev_font.render(f"+{ev.points} pts", True, UI_COLORS["accent_gold"])
                surface.blit(desc_surf, (panel_x + 35, start_y + i * 26))
                surface.blit(val_surf, (panel_x + panel_w - 105, start_y + i * 26))

        # Buttons
        self.play_again_btn.draw(surface)
        self.menu_btn.draw(surface)
