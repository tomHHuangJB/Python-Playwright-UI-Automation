from __future__ import annotations

from playwright.sync_api import Locator, expect


class UiAssertions:
    @staticmethod
    def visible(locator: Locator) -> None:
        expect(locator).to_be_visible()

    @staticmethod
    def text(locator: Locator, value: str) -> None:
        expect(locator).to_contain_text(value)

    @staticmethod
    def value(locator: Locator, value: str) -> None:
        expect(locator).to_have_value(value)

    @staticmethod
    def absent(locator: Locator) -> None:
        expect(locator).to_have_count(0)
