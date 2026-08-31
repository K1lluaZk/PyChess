"""Text input box component for account username entry."""
import pygame
import time
from typing import Callable, Optional, Tuple

from config.settings import UI_COLORS
from ui.components.theme import get_font


class TextInput:
    """An interactive text input box with focus handling and cursor blinking."""

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        placeholder: str = "Enter username...",
        max_chars: int = 20,
        font_size: int = 18,
        on_submit: Optional[Callable[[str], None]] = None,
    ):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.max_chars = max_chars
        self.font_size = font_size
        self.on_submit = on_submit
        self.text = ""
        self.is_active = False
        self.cursor_visible = True
        self.last_cursor_toggle = time.time()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles focus click and keyboard input."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_active = self.rect.collidepoint(event.pos)
            return self.is_active

        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                if self.on_submit and self.text.strip():
                    self.on_submit(self.text.strip())
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return True
            else:
                if len(self.text) < self.max_chars and event.unicode.isprintable():
                    self.text += event.unicode
                    return True
        return False

    def update(self) -> None:
        """Blink cursor timer."""
        now = time.time()
        if now - self.last_cursor_toggle > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = now

    def draw(self, surface: pygame.Surface) -> None:
        """Render the input box."""
        # Box background
        bg = UI_COLORS["bg_card"] if not self.is_active else (48, 54, 64)
        border = UI_COLORS["accent_blue"] if self.is_active else UI_COLORS["border"]
        pygame.draw.rect(surface, bg, self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, width=2 if self.is_active else 1, border_radius=6)

        font = get_font(self.font_size)
        if self.text:
            display_text = self.text
            text_color = UI_COLORS["text_primary"]
        else:
            display_text = self.placeholder
            text_color = UI_COLORS["text_secondary"]

        text_surf = font.render(display_text, True, text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 12, self.rect.centery))
        surface.blit(text_surf, text_rect)

        # Draw cursor
        if self.is_active and self.cursor_visible:
            cursor_x = text_rect.right + 2 if self.text else self.rect.x + 12
            pygame.draw.line(
                surface,
                UI_COLORS["text_primary"],
                (cursor_x, self.rect.y + 8),
                (cursor_x, self.rect.bottom - 8),
                2,
            )
