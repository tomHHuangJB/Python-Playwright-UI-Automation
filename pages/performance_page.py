from __future__ import annotations

from playwright.sync_api import Locator

from components.header import Header
from pages.base_page import BasePage


class PerformancePage(BasePage):
    PATH = "/performance"

    def __init__(self, page) -> None:
        super().__init__(page)
        self.header = Header(page)
        self.large_dom = self.by_test_id("large-dom")
        self.block_main_thread_button = self.by_test_id("block-main-thread")
        self.worker_result = self.by_test_id("worker-result")
        self.cpu_indicator = self.by_test_id("cpu-indicator")

    @property
    def lazy_images(self) -> Locator:
        return self.page.get_by_role("img", name="lazy")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        self.expect_visible(self.large_dom)
        self.expect_visible(self.block_main_thread_button)
        self.expect_visible(self.worker_result)
        self.expect_visible(self.cpu_indicator)

    def wait_for_large_dom_render(self, min_count: int = 100) -> None:
        self.page.wait_for_function(
            """
            ([selector, count]) => document.querySelectorAll(selector).length > count
            """,
            arg=["[data-testid='large-dom'] span", min_count],
        )

    def large_dom_count(self) -> int:
        return self.large_dom.locator("span").count()

    def block_main_thread(self) -> None:
        self.block_main_thread_button.click()
