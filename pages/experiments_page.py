from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class ExperimentsPage(BasePage):
    PATH = "/experiments"
    ROUTE_NAME = "experiments"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def variant_a_button(self):
        return self.by_test_id("variant-a")

    @property
    def variant_b_button(self):
        return self.by_test_id("variant-b")

    @property
    def active_variant_label(self):
        return self.page.get_by_text("Active variant:")

    @property
    def flag_override_button(self):
        return self.by_test_id("flag-override")

    @property
    def role_select(self):
        return self.by_test_id("role-select")

    @property
    def flag_enabled_label(self):
        return self.page.get_by_text("Flag enabled:")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.variant_a_button).to_be_visible()
        expect(self.variant_b_button).to_be_visible()
        expect(self.flag_override_button).to_be_visible()
        expect(self.role_select).to_be_visible()

    def choose_variant_a(self) -> None:
        self.variant_a_button.click()

    def choose_variant_b(self) -> None:
        self.variant_b_button.click()

    def apply_flag_override(self) -> None:
        self.flag_override_button.click()

    def select_role(self, role: str) -> None:
        self.role_select.select_option(role)
