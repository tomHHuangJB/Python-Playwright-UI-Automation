from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class I18nPage(BasePage):
    PATH = "/i18n"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def locale_select(self):
        return self.by_test_id("locale-select")

    @property
    def timezone_select(self):
        return self.by_test_id("timezone-select")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.locale_select).to_be_visible()
        expect(self.timezone_select).to_be_visible()

    def set_locale(self, value: str) -> None:
        self.locale_select.select_option(value)

    def set_timezone(self, value: str) -> None:
        self.timezone_select.select_option(value)
