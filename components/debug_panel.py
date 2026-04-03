from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DebugPanel(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def panel(self):
        return self.by_role("dialog", name="Debug panel")

    @property
    def close_button(self):
        return self.by_test_id("debug-close")

    @property
    def show_test_ids_toggle(self):
        return self.by_test_id("debug-testids")

    @property
    def network_profile_select(self):
        return self.by_test_id("debug-network")

    @property
    def offline_toggle(self):
        return self.by_test_id("debug-offline")

    @property
    def time_skew_input(self):
        return self.by_test_id("debug-time-skew")

    @property
    def permission_override_select(self):
        return self.by_test_id("debug-permission")

    @property
    def error_log_viewer(self):
        return self.by_test_id("error-log-viewer")

    @property
    def api_log_viewer(self):
        return self.by_test_id("api-log-viewer")

    @property
    def state_viewer(self):
        return self.by_test_id("state-viewer")

    def open(self) -> None:
        self.page.keyboard.press("Alt+Shift+D")

    def close(self) -> None:
        self.close_button.click()

    def expect_open(self) -> None:
        expect(self.panel).to_be_visible()

    def expect_closed(self) -> None:
        expect(self.panel).to_have_count(0)

    def enable_test_ids(self) -> None:
        if not self.show_test_ids_toggle.is_checked():
            self.show_test_ids_toggle.click()

    def toggle_offline(self) -> None:
        self.offline_toggle.click()

    def select_network_profile(self, profile: str) -> None:
        self.network_profile_select.select_option(profile)

    def select_permission_override(self, value: str) -> None:
        self.permission_override_select.select_option(value)

    def set_time_skew(self, value: str) -> None:
        self.time_skew_input.fill(value)

    def expect_test_ids_visible(self) -> None:
        expect(self.css("html")).to_have_attribute("data-testid-visible", "true")
