from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class IntegrationsPage(BasePage):
    PATH = "/integrations"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def payment_iframe(self):
        return self.by_test_id("payment-iframe")

    @property
    def iframe_message(self):
        return self.by_test_id("iframe-message")

    @property
    def csp_note(self):
        return self.by_test_id("csp-note")

    @property
    def csp_iframe(self):
        return self.by_test_id("csp-iframe")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.payment_iframe).to_be_visible()
        expect(self.csp_note).to_be_visible()
        expect(self.csp_iframe).to_be_visible()

    def approve_payment_in_iframe(self) -> None:
        frame = self.page.frame_locator("[data-testid='payment-iframe']")
        frame.get_by_role("button", name="Approve Payment").click()
