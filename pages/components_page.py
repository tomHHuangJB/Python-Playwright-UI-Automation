from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class ComponentsPage(BasePage):
    PATH = "/components"
    ROUTE_NAME = "components"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def virtual_list(self):
        return self.by_test_id("virtual-list")

    @property
    def infinite_scroll(self):
        return self.by_test_id("infinite-scroll")

    @property
    def load_more_button(self):
        return self.by_test_id("load-more")

    @property
    def svg_chart(self):
        return self.by_test_id("svg-chart")

    @property
    def canvas(self):
        return self.by_test_id("canvas")

    @property
    def context_zone(self):
        return self.by_test_id("context-zone")

    @property
    def toast_button(self):
        return self.by_test_id("toast-btn")

    @property
    def toast_items(self):
        return self.page.get_by_test_id("toast-item")

    @property
    def active_bar_label(self):
        return self.page.get_by_text("Selected bar:")

    @property
    def tooltip_trigger(self):
        return self.page.get_by_text("Hover tooltip")

    @property
    def tooltip_content(self):
        return self.page.get_by_text("Delayed tooltip content")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.virtual_list).to_be_visible()
        expect(self.infinite_scroll).to_be_visible()
        expect(self.svg_chart).to_be_visible()
        expect(self.canvas).to_be_visible()

    def infinite_items_count(self) -> int:
        return self.infinite_scroll.locator("div.rounded").count()

    def load_more_items(self) -> None:
        self.load_more_button.click()

    def select_bar_b(self) -> None:
        self.svg_chart.locator("rect").nth(1).click()

    def open_context_menu(self) -> None:
        self.context_zone.click(button="right")

    def trigger_toast(self) -> None:
        self.toast_button.click()
