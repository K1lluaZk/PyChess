"""Configuration module for PyChess.

Defines display settings, board color themes, UI palettes, and asset paths.
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PIECES_DIR = os.path.join(ASSETS_DIR, "images", "pieces")
LEGACY_PIECES_DIR = os.path.join(BASE_DIR, "Src", "Pieces")

# Window & Display
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 620
FPS = 60

# Chess Board Dimensions
BOARD_ROWS = 8
BOARD_COLS = 8
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // BOARD_COLS  # 60px
BOARD_OFFSET_X = 40
BOARD_OFFSET_Y = 70

# Color Themes for Chess Board
BOARD_THEMES = {
    "Classic Slate": {
        "light": (232, 235, 239),
        "dark": (125, 135, 150),
        "highlight": (100, 220, 100, 140),
        "last_move": (255, 235, 120, 110),
        "check": (230, 60, 60, 160),
    },
    "Emerald Forest": {
        "light": (238, 238, 210),
        "dark": (118, 150, 86),
        "highlight": (186, 202, 68, 160),
        "last_move": (246, 246, 130, 120),
        "check": (230, 60, 60, 160),
    },
    "Ocean Breeze": {
        "light": (225, 235, 245),
        "dark": (95, 135, 175),
        "highlight": (80, 200, 220, 150),
        "last_move": (240, 230, 140, 120),
        "check": (230, 60, 60, 160),
    },
    "Warm Wood": {
        "light": (240, 217, 181),
        "dark": (181, 136, 99),
        "highlight": (130, 210, 120, 150),
        "last_move": (230, 210, 110, 120),
        "check": (230, 60, 60, 160),
    },
}

# UI Theme Colors (Modern Dark Palette)
UI_COLORS = {
    "bg_dark": (22, 27, 34),
    "bg_panel": (33, 38, 45),
    "bg_card": (40, 46, 54),
    "border": (56, 63, 72),
    "text_primary": (240, 246, 252),
    "text_secondary": (139, 148, 158),
    "accent_primary": (46, 160, 67),
    "accent_hover": (63, 185, 80),
    "accent_blue": (31, 111, 235),
    "accent_blue_hover": (56, 139, 253),
    "accent_gold": (210, 153, 34),
    "accent_red": (218, 54, 51),
    "accent_red_hover": (248, 81, 73),
}

# Sound Settings (defaults)
DEFAULT_SETTINGS = {
    "board_theme": "Classic Slate",
    "sound_enabled": True,
    "highlight_moves": True,
    "ai_difficulty": "Normal",
}
