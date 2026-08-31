"""Interactive Pygame Button component with hover animation and callbacks."""
import pygame
from typing import Callable, Optional, Tuple

from config.settings import UI_COLORS
from ui.components.theme import get_font


class Button:
    """A responsive UI button with hover animations and click callbacks."""

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        bg_color: Tuple[int, int, int] = UI_COLORS["accent_blue"],
        hover_color: Tuple[int, int, int] = UI_COLORS["accent_blue_hover"],
        text_color: Tuple[int, int, int] = UI_COLORS["text_primary"],
        font_size: int = 20,
        border_radius: int = 8,
        icon: Optional[str] = None,
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.icon = icon
        self.is_hovered: bool = False
        self.is_disabled: bool = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles mouse move and click events. Returns True if button was clicked."""
        if self.is_disabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover state based on mouse position."""
        if not self.is_disabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        """Render the button to the target surface."""
        color = (60, 65, 75) if self.is_disabled else (self.hover_color if self.is_hovered else self.bg_color)

        # Button shadow / background
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(
            surface,
            UI_COLORS["border"],
            self.rect,
            width=1,
            border_radius=self.border_radius,
        )

        # Render label
        font = get_font(self.font_size, bold=True)
        label = f"{self.icon} {self.text}" if self.icon else self.text
        text_surf = font.render(label, True, (120, 130, 140) if self.is_disabled else self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
