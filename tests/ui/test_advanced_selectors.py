from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.auth_page import AuthPage
from pages.components_page import ComponentsPage


@pytest.mark.ui
def test_advanced_locator_patterns(page) -> None:
    components_page = ComponentsPage(page)
    auth_page = AuthPage(page)

    components_page.open()
    components_page.expect_page_ready()

    page.once("dialog", lambda dialog: dialog.accept())
    components_page.open_context_menu()

    components_page.toast_button.scroll_into_view_if_needed()
    components_page.trigger_toast()
    expect(components_page.toast_items.first).to_be_visible()

    auth_page.open()
    auth_page.expect_page_ready()
    auth_page.username_input.fill("relative-locator")
    expect(auth_page.username_input).to_have_value("relative-locator")
