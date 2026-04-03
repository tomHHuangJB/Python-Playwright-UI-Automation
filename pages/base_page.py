from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    PATH = "/"
    ROUTE_NAME = "base"

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, path: str) -> None:
        self.page.goto(path, wait_until="domcontentloaded")

    def open(self) -> None:
        self.goto(self.PATH)

    def by_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    def wait_for_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)

    @classmethod
    def route_name(cls) -> str:
        return cls.ROUTE_NAME

    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def expect_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_contain_text(text)
