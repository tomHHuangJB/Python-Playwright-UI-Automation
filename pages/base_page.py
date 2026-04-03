from __future__ import annotations

from typing import Any, cast

from playwright.sync_api import FrameLocator, Locator, Page, expect


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

    def by_test_id_prefix(self, prefix: str) -> Locator:
        return self.page.locator(f"[data-testid^='{prefix}']")

    def frame_by_test_id(self, test_id: str) -> FrameLocator:
        return self.page.frame_locator(f"[data-testid='{test_id}']")

    def by_role(self, role: str, name: str | None = None) -> Locator:
        return self.page.get_by_role(cast(Any, role), name=name)

    def by_text(self, text: str) -> Locator:
        return self.page.get_by_text(text)

    def css(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def wait_for_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)

    @classmethod
    def route_name(cls) -> str:
        return cls.ROUTE_NAME

    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def expect_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_contain_text(text)
