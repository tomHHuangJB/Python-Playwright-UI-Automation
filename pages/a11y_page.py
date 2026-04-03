from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class A11yPage(BasePage):
    PATH = "/a11y"
    ROUTE_NAME = "a11y"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def aria_live_region(self):
        return self.by_test_id("aria-live")

    @property
    def announce_button(self):
        return self.by_test_id("announce-btn")

    @property
    def keyboard_trap(self):
        return self.by_test_id("keyboard-trap")

    @property
    def focus_modal(self):
        return self.by_test_id("focus-modal")

    @property
    def high_contrast_button(self):
        return self.by_test_id("high-contrast")

    @property
    def reduced_motion_button(self):
        return self.by_test_id("reduced-motion")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.aria_live_region).to_be_visible()
        expect(self.keyboard_trap).to_be_visible()
        expect(self.high_contrast_button).to_be_visible()

    def announce_update(self) -> None:
        self.announce_button.click()

    def open_modal(self) -> None:
        self.page.get_by_role("button", name="Open modal").click()

    def close_modal(self) -> None:
        self.focus_modal.get_by_role("button", name="Close").click()

    def expect_modal_focused(self) -> None:
        expect(self.focus_modal).to_be_focused()
