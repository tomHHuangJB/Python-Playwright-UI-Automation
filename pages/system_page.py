from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class SystemPage(BasePage):
    PATH = "/system"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def permission_geo_button(self):
        return self.by_test_id("perm-geo")

    @property
    def permission_notifications_button(self):
        return self.by_test_id("perm-notif")

    @property
    def permission_clipboard_button(self):
        return self.by_test_id("perm-clipboard")

    @property
    def permission_status_list(self):
        return self.by_test_id("perm-status-list")

    @property
    def permission_result(self):
        return self.by_test_id("perm-result")

    @property
    def dialog_alert_button(self):
        return self.by_test_id("dialog-alert")

    @property
    def dialog_confirm_button(self):
        return self.by_test_id("dialog-confirm")

    @property
    def dialog_prompt_button(self):
        return self.by_test_id("dialog-prompt")

    @property
    def dialog_result(self):
        return self.by_test_id("dialog-result")

    @property
    def window_open_button(self):
        return self.by_test_id("window-open")

    @property
    def window_status(self):
        return self.by_test_id("window-status")

    @property
    def storage_write_button(self):
        return self.by_test_id("storage-write")

    @property
    def storage_event(self):
        return self.by_test_id("storage-event")

    @property
    def role_access_select(self):
        return self.by_test_id("role-access-select")

    @property
    def role_permissions(self):
        return self.by_test_id("role-permissions")

    @property
    def role_admin_visibility(self):
        return self.by_test_id("role-admin-visibility")

    @property
    def role_destructive_action(self):
        return self.by_test_id("role-destructive-action")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.permission_geo_button).to_be_visible()
        expect(self.dialog_alert_button).to_be_visible()
        expect(self.role_access_select).to_be_visible()

    def request_geo_permission(self) -> None:
        self.permission_geo_button.click()

    def request_notification_permission(self) -> None:
        self.permission_notifications_button.click()

    def open_popup(self) -> None:
        self.window_open_button.click()

    def write_storage(self) -> None:
        self.storage_write_button.click()

    def set_role(self, role: str) -> None:
        self.role_access_select.select_option(role)
