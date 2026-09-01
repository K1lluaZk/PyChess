"""Account management and login screen."""
import pygame
from typing import List, TYPE_CHECKING

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, UI_COLORS
from database.models import User
from ui.screens.base_screen import BaseScreen
from ui.components.button import Button
from ui.components.text_input import TextInput
from ui.components.card import draw_panel, draw_badge
from ui.components.theme import get_font

if TYPE_CHECKING:
    from ui.screen_manager import ScreenManager


class AccountScreen(BaseScreen):
    """Allows user to log in, register a username, choose guest mode, or switch accounts."""

    def __init__(self, manager: "ScreenManager"):
        super().__init__(manager)
        self.message = ""
        self.message_color = UI_COLORS["text_secondary"]
        self.existing_users: List[User] = []
        self.user_buttons: List[Button] = []

        # Text input
        center_x = WINDOW_WIDTH // 2
        self.username_input = TextInput(
            (center_x - 170, 160, 230, 44),
            placeholder="Enter your username...",
            on_submit=self._handle_login_or_create,
        )

        self.login_btn = Button(
            (center_x + 70, 160, 100, 44),
            "Login",
            on_click=lambda: self._handle_login_or_create(self.username_input.text),
            bg_color=UI_COLORS["accent_primary"],
            hover_color=UI_COLORS["accent_hover"],
            font_size=16,
        )

        self.guest_btn = Button(
            (center_x - 170, 220, 340, 44),
            "Continue as Guest",
            on_click=self._handle_guest_login,
            bg_color=UI_COLORS["bg_card"],
            hover_color=(55, 62, 72),
            font_size=16,
        )

        self.back_btn = Button(
            (center_x - 170, 520, 340, 44),
            "Back to Main Menu",
            on_click=lambda: self.manager.switch_to("home"),
            bg_color=(45, 50, 60),
            hover_color=(60, 68, 80),
            font_size=16,
        )

    def enter(self) -> None:
        self.message = ""
        self._refresh_users_list()

    def _refresh_users_list(self) -> None:
        self.existing_users = self.manager.user_repo.get_top_players(limit=5)
        self.user_buttons.clear()

        start_y = 330
        center_x = WINDOW_WIDTH // 2
        for i, user in enumerate(self.existing_users):
            u_btn = Button(
                (center_x - 170, start_y + i * 36, 340, 32),
                f"{user.username} ({user.points:,} pts)",
                on_click=lambda u=user: self._select_user(u),
                bg_color=UI_COLORS["bg_card"],
                hover_color=UI_COLORS["accent_blue"],
                font_size=14,
                border_radius=6,
            )
            self.user_buttons.append(u_btn)

    def _handle_login_or_create(self, name: str) -> None:
        clean = name.strip()
        if not clean:
            self.message = "Please enter a valid username."
            self.message_color = UI_COLORS["accent_red"]
            return

        user = self.manager.user_repo.get_or_create_user(clean)
        if user:
            self.manager.session.login_user(user)
            self.message = f"Logged in as {user.username}!"
            self.message_color = UI_COLORS["accent_primary"]
            self._refresh_users_list()
            self.username_input.text = ""
        else:
            self.message = "Failed to load or create account."
            self.message_color = UI_COLORS["accent_red"]

    def _select_user(self, user: User) -> None:
        self.manager.session.login_user(user)
        self.message = f"Active account: {user.username}"
        self.message_color = UI_COLORS["accent_primary"]

    def _handle_guest_login(self) -> None:
        self.manager.session.login_as_guest()
        self.message = "Switched to Guest mode (Session points only)."
        self.message_color = UI_COLORS["accent_gold"]

    def handle_event(self, event: pygame.event.Event) -> None:
        self.username_input.handle_event(event)
        self.login_btn.handle_event(event)
        self.guest_btn.handle_event(event)
        self.back_btn.handle_event(event)
        for btn in self.user_buttons:
            btn.handle_event(event)

    def update(self) -> None:
        self.username_input.update()
        mouse_pos = pygame.mouse.get_pos()
        self.login_btn.update(mouse_pos)
        self.guest_btn.update(mouse_pos)
        self.back_btn.update(mouse_pos)
        for btn in self.user_buttons:
            btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(UI_COLORS["bg_dark"])

        panel_w, panel_h = 440, 550
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = 35
        draw_panel(surface, (panel_x, panel_y, panel_w, panel_h))

        # Title
        title_font = get_font(28, bold=True)
        title_surf = title_font.render("Player Accounts", True, UI_COLORS["text_primary"])
        surface.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH // 2, 70)))

        # Current status
        session = self.manager.session
        status_font = get_font(14)
        active_label = f"Current Profile: {session.get_display_name()}"
        stat_surf = status_font.render(active_label, True, UI_COLORS["accent_gold"] if session.is_guest else UI_COLORS["accent_primary"])
        surface.blit(stat_surf, stat_surf.get_rect(center=(WINDOW_WIDTH // 2, 105)))

        # Notice/Status feedback message
        if self.message:
            msg_font = get_font(13)
            m_surf = msg_font.render(self.message, True, self.message_color)
            surface.blit(m_surf, m_surf.get_rect(center=(WINDOW_WIDTH // 2, 132)))

        # Draw components
        self.username_input.draw(surface)
        self.login_btn.draw(surface)
        self.guest_btn.draw(surface)

        # Quick Select Section
        sec_font = get_font(14, bold=True)
        sec_surf = sec_font.render("Quick Select Existing Accounts:", True, UI_COLORS["text_secondary"])
        surface.blit(sec_surf, (panel_x + 50, 290))

        if not self.user_buttons:
            empty_font = get_font(13)
            e_surf = empty_font.render("No registered accounts yet.", True, UI_COLORS["text_secondary"])
            surface.blit(e_surf, (panel_x + 50, 330))
        else:
            for btn in self.user_buttons:
                btn.draw(surface)

        self.back_btn.draw(surface)
