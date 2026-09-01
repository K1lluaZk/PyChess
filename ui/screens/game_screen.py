"""Active chess game screen with board rendering, side stats panel, and controls."""
import pygame
from typing import TYPE_CHECKING

from config.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_ROWS,
    BOARD_COLS,
    BOARD_SIZE,
    SQUARE_SIZE,
    BOARD_OFFSET_X,
    BOARD_OFFSET_Y,
    UI_COLORS,
)
from game.constants import WHITE, BLACK, WHITE_KING, BLACK_KING
from game.game_state import GameState, GameStatus
from ui.screens.base_screen import BaseScreen
from ui.components.button import Button
from ui.components.card import draw_panel, draw_badge
from ui.components.theme import get_font, load_piece_images, get_board_theme

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class GameScreen(BaseScreen):
    """Main chess gameplay screen."""

    def __init__(self, manager: "ScreenManager"):
        super().__init__(manager)
        self.game_state = GameState()
        self.piece_images = load_piece_images(SQUARE_SIZE)
        self.small_piece_images = load_piece_images(24)

        # Side panel buttons
        panel_x = BOARD_OFFSET_X + BOARD_SIZE + 30
        self.restart_btn = Button(
            (panel_x, 500, 125, 42),
            "Restart",
            on_click=self._restart_game,
            bg_color=UI_COLORS["bg_card"],
            hover_color=(55, 62, 72),
            font_size=15,
        )
        self.menu_btn = Button(
            (panel_x + 135, 500, 125, 42),
            "Main Menu",
            on_click=self._return_to_menu,
            bg_color=(50, 25, 25),
            hover_color=UI_COLORS["accent_red_hover"],
            font_size=15,
        )

    def enter(self) -> None:
        """Reset or start a fresh match upon entering."""
        self.game_state.reset()
        self.piece_images = load_piece_images(SQUARE_SIZE)

    def _restart_game(self) -> None:
        self.game_state.reset()

    def _return_to_menu(self) -> None:
        self.manager.switch_to("home")

    def handle_event(self, event: pygame.event.Event) -> None:
        self.restart_btn.handle_event(event)
        self.menu_btn.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            # Check if clicked inside board area
            if (
                BOARD_OFFSET_X <= x < BOARD_OFFSET_X + BOARD_SIZE
                and BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + BOARD_SIZE
            ):
                col = (x - BOARD_OFFSET_X) // SQUARE_SIZE
                row = (y - BOARD_OFFSET_Y) // SQUARE_SIZE
                move_executed = self.game_state.handle_square_click(row, col)

                # Check if game ended
                if self.game_state.status in (GameStatus.CHECKMATE, GameStatus.STALEMATE):
                    # Award points to player session
                    pts_earned = self.game_state.points_engine.total_points
                    self.manager.session.award_match_points(pts_earned)
                    if self.manager.session.current_user:
                        self.manager.user_repo.record_match(
                            self.manager.session.current_user.id,
                            self.game_state.winner or "Tie",
                            pts_earned,
                            self.game_state.moves_count,
                        )
                    # Transition to result screen
                    self.manager.switch_to(
                        "result",
                        winner=self.game_state.winner,
                        points=pts_earned,
                        events=self.game_state.points_engine.get_breakdown(),
                        moves=self.game_state.moves_count,
                    )

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.restart_btn.update(mouse_pos)
        self.menu_btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(UI_COLORS["bg_dark"])

        # Load active board theme
        theme_name = self.manager.settings.get("board_theme", "Classic Slate")
        theme = get_board_theme(theme_name)

        # Draw Chess Board
        self._draw_board(surface, theme)

        # Draw Last Move Highlights
        if self.manager.settings.get("highlight_moves", True) and self.game_state.last_move:
            self._draw_last_move(surface, theme)

        # Draw Selected Square Highlight
        if self.game_state.selected_square:
            self._draw_selected_square(surface, theme)

        # Draw Valid Move Indicators
        if self.game_state.valid_moves:
            self._draw_valid_moves(surface, theme)

        # Draw King in Check Highlight
        if self.game_state.status == GameStatus.CHECK:
            self._draw_check_warning(surface, theme)

        # Draw Pieces
        self._draw_pieces(surface)

        # Draw Board Border Coordinates
        self._draw_coordinates(surface)

        # Draw Side Information Panel
        self._draw_side_panel(surface)

    def _draw_board(self, surface: pygame.Surface, theme: dict) -> None:
        """Draw standard 8x8 alternating checkered squares."""
        # Board shadow frame
        pygame.draw.rect(
            surface,
            (15, 18, 24),
            (BOARD_OFFSET_X - 6, BOARD_OFFSET_Y - 6, BOARD_SIZE + 12, BOARD_SIZE + 12),
            border_radius=4,
        )
        pygame.draw.rect(
            surface,
            UI_COLORS["border"],
            (BOARD_OFFSET_X - 2, BOARD_OFFSET_Y - 2, BOARD_SIZE + 4, BOARD_SIZE + 4),
            width=2,
            border_radius=2,
        )

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                color = theme["light"] if (row + col) % 2 == 0 else theme["dark"]
                sq_rect = pygame.Rect(
                    BOARD_OFFSET_X + col * SQUARE_SIZE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pygame.draw.rect(surface, color, sq_rect)

    def _draw_last_move(self, surface: pygame.Surface, theme: dict) -> None:
        """Subtle highlight on origin and destination squares of the last move."""
        highlight_color = theme.get("last_move", (255, 235, 120, 110))
        high_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        high_surf.fill(highlight_color)

        origin, dest = self.game_state.last_move
        for r, c in (origin, dest):
            surface.blit(
                high_surf,
                (BOARD_OFFSET_X + c * SQUARE_SIZE, BOARD_OFFSET_Y + r * SQUARE_SIZE),
            )

    def _draw_selected_square(self, surface: pygame.Surface, theme: dict) -> None:
        """Highlight the currently selected piece."""
        r, c = self.game_state.selected_square
        high_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        high_surf.fill((100, 200, 255, 130))
        surface.blit(
            high_surf,
            (BOARD_OFFSET_X + c * SQUARE_SIZE, BOARD_OFFSET_Y + r * SQUARE_SIZE),
        )

    def _draw_valid_moves(self, surface: pygame.Surface, theme: dict) -> None:
        """Highlight all destination targets for the selected piece."""
        for r, c in self.game_state.valid_moves:
            target_piece = self.game_state.board.get_piece(r, c)
            center_x = BOARD_OFFSET_X + c * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = BOARD_OFFSET_Y + r * SQUARE_SIZE + SQUARE_SIZE // 2

            if target_piece:  # Capture target: draw ring around square
                cap_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(
                    cap_surf,
                    (230, 70, 70, 180),
                    (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                    SQUARE_SIZE // 2 - 4,
                    width=4,
                )
                surface.blit(
                    cap_surf,
                    (BOARD_OFFSET_X + c * SQUARE_SIZE, BOARD_OFFSET_Y + r * SQUARE_SIZE),
                )
            else:  # Empty square: small center circle
                dot_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(
                    dot_surf,
                    theme.get("highlight", (100, 220, 100, 140)),
                    (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                    SQUARE_SIZE // 6,
                )
                surface.blit(
                    dot_surf,
                    (BOARD_OFFSET_X + c * SQUARE_SIZE, BOARD_OFFSET_Y + r * SQUARE_SIZE),
                )

    def _draw_check_warning(self, surface: pygame.Surface, theme: dict) -> None:
        """Draw red check alert indicator over the king under check."""
        king_pos = self.game_state.board.find_king(self.game_state.turn)
        if king_pos:
            r, c = king_pos
            warn_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            warn_surf.fill(theme.get("check", (230, 60, 60, 160)))
            surface.blit(
                warn_surf,
                (BOARD_OFFSET_X + c * SQUARE_SIZE, BOARD_OFFSET_Y + r * SQUARE_SIZE),
            )

    def _draw_pieces(self, surface: pygame.Surface) -> None:
        """Blit piece images onto their respective squares."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.game_state.board.get_piece(row, col)
                if piece and piece in self.piece_images:
                    surface.blit(
                        self.piece_images[piece],
                        (BOARD_OFFSET_X + col * SQUARE_SIZE, BOARD_OFFSET_Y + row * SQUARE_SIZE),
                    )

    def _draw_coordinates(self, surface: pygame.Surface) -> None:
        """Draw rank (1-8) and file (a-h) labels around the board."""
        font = get_font(12, bold=True)
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]

        for i in range(8):
            # Files (bottom)
            f_surf = font.render(files[i], True, UI_COLORS["text_secondary"])
            surface.blit(
                f_surf,
                (BOARD_OFFSET_X + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 4, BOARD_OFFSET_Y + BOARD_SIZE + 6),
            )
            # Ranks (left)
            r_surf = font.render(ranks[i], True, UI_COLORS["text_secondary"])
            surface.blit(
                r_surf,
                (BOARD_OFFSET_X - 16, BOARD_OFFSET_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 6),
            )

    def _draw_side_panel(self, surface: pygame.Surface) -> None:
        """Draw player info, match points, turn indicator, captured pieces, and control buttons."""
        panel_w = 260
        panel_h = BOARD_SIZE
        panel_x = BOARD_OFFSET_X + BOARD_SIZE + 30
        panel_y = BOARD_OFFSET_Y

        draw_panel(surface, (panel_x, panel_y, panel_w, panel_h))

        # Header Profile Box
        session = self.manager.session
        profile_rect = (panel_x + 15, panel_y + 15, panel_w - 30, 60)
        draw_panel(surface, profile_rect, bg_color=UI_COLORS["bg_card"], border_radius=8)

        name_font = get_font(16, bold=True)
        p_name = session.get_display_name()
        n_surf = name_font.render(p_name, True, UI_COLORS["text_primary"])
        surface.blit(n_surf, (panel_x + 25, panel_y + 24))

        status_text = "GUEST" if session.is_guest else "ACCOUNT"
        status_color = UI_COLORS["text_secondary"] if session.is_guest else UI_COLORS["accent_primary"]
        draw_badge(surface, (panel_x + panel_w - 95, panel_y + 24, 70, 22), status_text, text_color=status_color, font_size=11)

        # Match Points Counter
        pts_font = get_font(13)
        pts_label = f"Match Points: +{self.game_state.points_engine.total_points}"
        pt_surf = pts_font.render(pts_label, True, UI_COLORS["accent_gold"])
        surface.blit(pt_surf, (panel_x + 25, panel_y + 48))

        # Turn Indicator Box
        turn_rect = (panel_x + 15, panel_y + 90, panel_w - 30, 48)
        turn_bg = (35, 55, 45) if self.game_state.turn == WHITE else (50, 40, 45)
        draw_panel(surface, turn_rect, bg_color=turn_bg, border_radius=8)

        turn_font = get_font(15, bold=True)
        if self.game_state.status == GameStatus.CHECK:
            turn_label = "CHECK! White King under attack" if self.game_state.turn == WHITE else "CHECK! Black King under attack"
            turn_color = UI_COLORS["accent_red"]
        else:
            turn_label = "White's Turn (You)" if self.game_state.turn == WHITE else "Black's Turn (AI)"
            turn_color = UI_COLORS["text_primary"]

        t_surf = turn_font.render(turn_label, True, turn_color)
        surface.blit(t_surf, t_surf.get_rect(center=(panel_x + panel_w // 2, panel_y + 114)))

        # Move Counter
        move_font = get_font(13)
        m_surf = move_font.render(f"Moves: {self.game_state.moves_count}", True, UI_COLORS["text_secondary"])
        surface.blit(m_surf, (panel_x + 20, panel_y + 155))

        # Captured Pieces Section
        cap_title_font = get_font(14, bold=True)
        cap_surf = cap_title_font.render("Captured from AI:", True, UI_COLORS["text_secondary"])
        surface.blit(cap_surf, (panel_x + 20, panel_y + 185))

        # Render mini captured pieces icons
        start_x = panel_x + 20
        start_y = panel_y + 210
        for i, piece in enumerate(self.game_state.captured_by_white):
            if piece in self.small_piece_images:
                col_offset = (i % 8) * 26
                row_offset = (i // 8) * 28
                surface.blit(self.small_piece_images[piece], (start_x + col_offset, start_y + row_offset))

        # Recent Point Events list
        events_title = cap_title_font.render("Recent Point Events:", True, UI_COLORS["text_secondary"])
        surface.blit(events_title, (panel_x + 20, panel_y + 295))

        events = self.game_state.points_engine.get_breakdown()[-4:]
        if not events:
            none_font = get_font(13)
            no_ev_surf = none_font.render("No points scored yet", True, (100, 110, 120))
            surface.blit(no_ev_surf, (panel_x + 20, panel_y + 325))
        else:
            for idx, ev in enumerate(events):
                ev_font = get_font(12)
                ev_surf = ev_font.render(f"+{ev.points}  {ev.description}", True, UI_COLORS["accent_gold"])
                surface.blit(ev_surf, (panel_x + 20, panel_y + 322 + idx * 22))

        # Control Buttons
        self.restart_btn.draw(surface)
        self.menu_btn.draw(surface)
