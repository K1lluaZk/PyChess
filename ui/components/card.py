"""Card and panel container rendering utilities."""
import pygame
from typing import Optional, Tuple
from config.settings import UI_COLORS


def draw_panel(
    surface: pygame.Surface,
    rect: Tuple[int, int, int, int],
    bg_color: Tuple[int, int, int] = UI_COLORS["bg_panel"],
    border_color: Tuple[int, int, int] = UI_COLORS["border"],
    border_radius: int = 12,
    border_width: int = 1,
) -> None:
    """Draws a rounded rectangular panel."""
    r = pygame.Rect(rect)
    pygame.draw.rect(surface, bg_color, r, border_radius=border_radius)
    if border_width > 0:
        pygame.draw.rect(surface, border_color, r, width=border_width, border_radius=border_radius)


def draw_badge(
    surface: pygame.Surface,
    rect: Tuple[int, int, int, int],
    text: str,
    bg_color: Tuple[int, int, int] = UI_COLORS["bg_card"],
    text_color: Tuple[int, int, int] = UI_COLORS["accent_gold"],
    font_size: int = 14,
) -> None:
    """Draws a small status pill / badge."""
    from ui.components.theme import get_font

    r = pygame.Rect(rect)
    pygame.draw.rect(surface, bg_color, r, border_radius=12)
    pygame.draw.rect(surface, UI_COLORS["border"], r, width=1, border_radius=12)

    font = get_font(font_size, bold=True)
    surf = font.render(text, True, text_color)
    surface.blit(surf, surf.get_rect(center=r.center))
