from __future__ import annotations

from playwright.sync_api import Page, expect

from components.header import Header
from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"
    ROUTE_NAME = "home"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = Header(page)

    @property
    def session_state_card(self):
        return self.by_test_id("session-state")

    @property
    def notification_log(self):
        return self.by_test_id("notification-log")

    @property
    def websocket_status(self):
        return self.by_test_id("ws-status")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.session_state_card).to_be_visible()
        expect(self.notification_log).to_be_visible()
        expect(self.websocket_status).to_be_visible()

    def expect_authenticated_session(self) -> None:
        expect(self.session_state_card).to_contain_text("Authenticated")

    def expect_websocket_state(self, expected_status: str) -> None:
        expect(self.websocket_status).to_contain_text(expected_status)
