from __future__ import annotations

from playwright.sync_api import Page, expect


class DebugPanel:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def panel(self):
        return self.page.get_by_role("dialog", name="Debug panel")

    @property
    def close_button(self):
        return self.page.get_by_test_id("debug-close")

    @property
    def show_test_ids_toggle(self):
        return self.page.get_by_test_id("debug-testids")

    @property
    def network_profile_select(self):
        return self.page.get_by_test_id("debug-network")

    @property
    def permission_override_select(self):
        return self.page.get_by_test_id("debug-permission")

    @property
    def state_viewer(self):
        return self.page.get_by_test_id("state-viewer")

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

    def expect_test_ids_visible(self) -> None:
        expect(self.page.locator("html")).to_have_attribute("data-testid-visible", "true")
