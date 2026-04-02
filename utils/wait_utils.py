from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class WaitUtils:
    def __init__(self, page: Page) -> None:
        self.page = page

    def for_url_contains(self, value: str) -> None:
        self.page.wait_for_url(f"**{value}*")

    def for_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def for_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_contain_text(text)
