from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from components.debug_panel import DebugPanel


@pytest.mark.ui
def test_debug_panel_controls(page) -> None:
    page.goto("/")

    debug_panel = DebugPanel(page)

    debug_panel.open()
    debug_panel.expect_open()

    debug_panel.enable_test_ids()
    debug_panel.expect_test_ids_visible()

    debug_panel.toggle_offline()
    debug_panel.select_network_profile("offline")
    debug_panel.select_permission_override("granted")
    debug_panel.set_time_skew("60000")

    expect(debug_panel.state_viewer).to_contain_text("Network: offline")
    expect(debug_panel.state_viewer).to_contain_text("Permissions: granted")
    expect(debug_panel.error_log_viewer).to_be_visible()
    expect(debug_panel.api_log_viewer).to_be_visible()
    expect(debug_panel.error_log_viewer).to_contain_text("No errors logged.")
    expect(debug_panel.api_log_viewer).to_contain_text(
        re.compile(r"No responses logged\.|Recent API Responses")
    )
