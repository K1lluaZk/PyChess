"""Theme, font, and piece asset loading utilities."""
import os
import pygame
from typing import Dict, Optional, Tuple

from config.settings import (
    ASSETS_DIR,
    PIECES_DIR,
    LEGACY_PIECES_DIR,
    SQUARE_SIZE,
    UI_COLORS,
    BOARD_THEMES,
)

# Global piece image cache
_PIECE_CACHE: Dict[Tuple[str, int], pygame.Surface] = {}
_FONT_CACHE: Dict[Tuple[str, int, bool], pygame.font.Font] = {}


def get_font(size: int = 18, bold: bool = False, font_name: Optional[str] = None) -> pygame.font.Font:
    """Returns cached SysFont or default pygame font."""
    key = (font_name or "Segoe UI", size, bold)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = pygame.font.SysFont(font_name or "Segoe UI, Arial, sans-serif", size, bold=bold)
        except Exception:
            _FONT_CACHE[key] = pygame.font.Font(None, size)
    return _FONT_CACHE[key]


def load_piece_images(size: int = SQUARE_SIZE) -> Dict[str, pygame.Surface]:
    """Loads and scales all 12 piece images from assets or legacy Src folder."""
    pieces = {}
    piece_names = ["wp", "bp", "wr", "br", "wn", "bn", "wb", "bb", "wq", "bq", "wk", "bk"]

    for name in piece_names:
        cache_key = (name, size)
        if cache_key in _PIECE_CACHE:
            pieces[name] = _PIECE_CACHE[cache_key]
            continue

        # Try assets directory first, then legacy directory
        path = os.path.join(PIECES_DIR, f"{name}.png")
        if not os.path.exists(path):
            path = os.path.join(LEGACY_PIECES_DIR, f"{name}.png")

        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                scaled = pygame.transform.smoothscale(img, (size, size))
                _PIECE_CACHE[cache_key] = scaled
                pieces[name] = scaled
            except Exception:
                # Fallback to direct scale
                img = pygame.image.load(path)
                scaled = pygame.transform.scale(img, (size, size))
                _PIECE_CACHE[cache_key] = scaled
                pieces[name] = scaled
        else:
            # Fallback surface if image missing
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 200, 200) if name.startswith("w") else (50, 50, 50), (size // 2, size // 2), size // 3)
            pieces[name] = surf

    return pieces


def get_board_theme(theme_name: str) -> dict:
    """Returns colors for selected board theme with fallback."""
    return BOARD_THEMES.get(theme_name, BOARD_THEMES["Classic Slate"])
