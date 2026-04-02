from __future__ import annotations

import pytest
from playwright.sync_api import Dialog, expect

from pages.system_page import SystemPage


@pytest.mark.regression
def test_system_permissions_dialogs_storage_and_roles(page) -> None:
    page.add_init_script(
        """
        Date.now = () => 1711987200000;
        window.open = () => ({ closed: false });
        """
    )

    system_page = SystemPage(page)

    dialog_answers = iter(["accept", "accept", "typed-value"])

    def handle_dialog(dialog: Dialog) -> None:
        answer = next(dialog_answers)
        if dialog.type == "prompt":
            dialog.accept("typed-value")
        elif answer == "accept":
            dialog.accept()
        else:
            dialog.dismiss()

    page.on("dialog", handle_dialog)

    system_page.open()
    system_page.expect_page_ready()

    expect(system_page.permission_status_list).to_contain_text("Clipboard: granted")

    system_page.request_geo_permission()
    expect(system_page.permission_result).to_contain_text("Geolocation => granted")
    expect(system_page.permission_status_list).to_contain_text("Geo: granted")

    system_page.request_notification_permission()
    expect(system_page.permission_result).to_contain_text("Notifications => denied")

    system_page.dialog_alert_button.click()
    expect(system_page.dialog_result).to_contain_text("Alert acknowledged")

    system_page.dialog_confirm_button.click()
    expect(system_page.dialog_result).to_contain_text("Confirm => accepted")

    system_page.dialog_prompt_button.click()
    expect(system_page.dialog_result).to_contain_text("Prompt => typed-value")

    system_page.open_popup()
    expect(system_page.window_status).to_contain_text("Popup opened")

    system_page.write_storage()
    expect(system_page.storage_event).to_contain_text("Local write: session-1711987200000")

    page.evaluate(
        """
        window.dispatchEvent(
          new StorageEvent("storage", {
            key: "session",
            newValue: "session-remote-sync"
          })
        );
        """
    )
    expect(system_page.storage_event).to_contain_text("Storage event sync: session-remote-sync")

    expect(system_page.role_permissions).to_contain_text("read")
    expect(system_page.role_admin_visibility).to_contain_text("hidden")
    expect(system_page.role_destructive_action).to_be_disabled()

    system_page.set_role("admin")
    expect(system_page.role_permissions).to_contain_text("all")
    expect(system_page.role_admin_visibility).to_contain_text("visible")
    expect(system_page.role_destructive_action).to_be_enabled()
