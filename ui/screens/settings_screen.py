"""Settings configuration screen."""
import pygame
from typing import List, TYPE_CHECKING

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, UI_COLORS, BOARD_THEMES
from ui.screens.base_screen import BaseScreen
from ui.components.button import Button
from ui.components.card import draw_panel
from ui.components.theme import get_font

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class SettingsScreen(BaseScreen):
    """Settings menu for board themes, visual highlights, and audio preferences."""

    def __init__(self, manager: "ScreenManager"):
        super().__init__(manager)
        self.theme_buttons: List[Button] = []
        self._init_theme_buttons()

        center_x = WINDOW_WIDTH // 2
        self.toggle_highlight_btn = Button(
            (center_x - 170, 360, 340, 44),
            "Highlight Valid Moves: ON",
            on_click=self._toggle_highlights,
            bg_color=UI_COLORS["bg_card"],
            hover_color=(55, 62, 72),
            font_size=15,
        )

        self.toggle_sound_btn = Button(
            (center_x - 170, 420, 340, 44),
            "Sound FX: ON",
            on_click=self._toggle_sound,
            bg_color=UI_COLORS["bg_card"],
            hover_color=(55, 62, 72),
            font_size=15,
        )

        self.back_btn = Button(
            (center_x - 170, 520, 340, 44),
            "Back to Main Menu",
            on_click=lambda: self.manager.switch_to("home"),
            bg_color=(45, 50, 60),
            hover_color=(60, 68, 80),
            font_size=16,
        )

    def _init_theme_buttons(self) -> None:
        self.theme_buttons.clear()
        themes = list(BOARD_THEMES.keys())
        center_x = WINDOW_WIDTH // 2
        start_y = 150
        for i, theme_name in enumerate(themes):
            btn = Button(
                (center_x - 170, start_y + i * 46, 340, 38),
                theme_name,
                on_click=lambda t=theme_name: self._set_theme(t),
                bg_color=UI_COLORS["bg_card"],
                hover_color=UI_COLORS["accent_blue"],
                font_size=14,
                border_radius=6,
            )
            self.theme_buttons.append(btn)

    def _set_theme(self, theme_name: str) -> None:
        self.manager.settings["board_theme"] = theme_name

    def _toggle_highlights(self) -> None:
        current = self.manager.settings.get("highlight_moves", True)
        self.manager.settings["highlight_moves"] = not current
        self.toggle_highlight_btn.text = f"Highlight Valid Moves: {'ON' if not current else 'OFF'}"

    def _toggle_sound(self) -> None:
        current = self.manager.settings.get("sound_enabled", True)
        self.manager.settings["sound_enabled"] = not current
        self.toggle_sound_btn.text = f"Sound FX: {'ON' if not current else 'OFF'}"

    def enter(self) -> None:
        hl = self.manager.settings.get("highlight_moves", True)
        self.toggle_highlight_btn.text = f"Highlight Valid Moves: {'ON' if hl else 'OFF'}"
        snd = self.manager.settings.get("sound_enabled", True)
        self.toggle_sound_btn.text = f"Sound FX: {'ON' if snd else 'OFF'}"

    def handle_event(self, event: pygame.event.Event) -> None:
        for btn in self.theme_buttons:
            btn.handle_event(event)
        self.toggle_highlight_btn.handle_event(event)
        self.toggle_sound_btn.handle_event(event)
        self.back_btn.handle_event(event)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        current_theme = self.manager.settings.get("board_theme", "Classic Slate")
        for btn in self.theme_buttons:
            btn.update(mouse_pos)
            if btn.text == current_theme:
                btn.bg_color = UI_COLORS["accent_blue"]
            else:
                btn.bg_color = UI_COLORS["bg_card"]

        self.toggle_highlight_btn.update(mouse_pos)
        self.toggle_sound_btn.update(mouse_pos)
        self.back_btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(UI_COLORS["bg_dark"])

        panel_w, panel_h = 440, 550
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = 35
        draw_panel(surface, (panel_x, panel_y, panel_w, panel_h))

        # Title
        title_font = get_font(28, bold=True)
        title_surf = title_font.render("Game Settings", True, UI_COLORS["text_primary"])
        surface.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH // 2, 70)))

        # Subtitle
        sub_font = get_font(14, bold=True)
        sub_surf = sub_font.render("Select Chess Board Theme:", True, UI_COLORS["text_secondary"])
        surface.blit(sub_surf, (panel_x + 50, 120))

        # Draw theme buttons
        for btn in self.theme_buttons:
            btn.draw(surface)
            # Draw color swatch preview next to theme button
            theme_data = BOARD_THEMES.get(btn.text)
            if theme_data:
                swatch_x = btn.rect.right - 45
                swatch_y = btn.rect.centery - 8
                pygame.draw.rect(surface, theme_data["light"], (swatch_x, swatch_y, 16, 16), border_radius=2)
                pygame.draw.rect(surface, theme_data["dark"], (swatch_x + 16, swatch_y, 16, 16), border_radius=2)

        # Draw other settings
        self.toggle_highlight_btn.draw(surface)
        self.toggle_sound_btn.draw(surface)
        self.back_btn.draw(surface)
