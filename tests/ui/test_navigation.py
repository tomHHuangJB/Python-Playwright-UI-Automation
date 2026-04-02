from __future__ import annotations

import pytest
from playwright.sync_api import expect

from components.debug_panel import DebugPanel
from components.header import Header
from flows.navigation_flow import NavigationFlow


@pytest.mark.ui
def test_primary_navigation_and_debug_panel(page) -> None:
    page.goto("/")

    header = Header(page)
    debug_panel = DebugPanel(page)
    navigation_flow = NavigationFlow(header, debug_panel)

    header.expect_loaded()

    navigation_flow.traverse_primary_routes()

    expect(page).to_have_url("http://localhost:5173/")
    navigation_flow.open_debug_panel()
    debug_panel.enable_test_ids()
    debug_panel.expect_test_ids_visible()
    expect(debug_panel.state_viewer).to_contain_text("Path: /")
    debug_panel.close()
    debug_panel.expect_closed()
