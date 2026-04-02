from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class MobilePage(BasePage):
    PATH = "/mobile"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def orientation_value(self):
        return self.by_test_id("orientation-value")

    @property
    def gesture_surface(self):
        return self.by_test_id("gesture-surface")

    @property
    def gesture_result(self):
        return self.by_test_id("gesture-result")

    @property
    def long_press_button(self):
        return self.by_test_id("long-press")

    @property
    def refresh_count(self):
        return self.by_test_id("refresh-count")

    @property
    def refresh_trigger(self):
        return self.by_test_id("refresh-trigger")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.orientation_value).to_be_visible()
        expect(self.gesture_surface).to_be_visible()
        expect(self.long_press_button).to_be_visible()
        expect(self.refresh_count).to_be_visible()

    def swipe_right(self) -> None:
        box = self.gesture_surface.bounding_box()
        if box is None:
            raise AssertionError("Gesture surface bounding box was not available")

        start_x = box["x"] + 20
        start_y = box["y"] + box["height"] / 2
        end_x = box["x"] + box["width"] - 20
        end_y = start_y

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(end_x, end_y, steps=8)
        self.page.mouse.up()

    def trigger_long_press(self) -> None:
        self.long_press_button.dispatch_event("contextmenu")

    def trigger_refresh(self) -> None:
        self.refresh_trigger.click()
