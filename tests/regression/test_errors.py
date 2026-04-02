from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.errors_page import ErrorsPage


@pytest.mark.regression
def test_errors_route_surfaces_failure_and_security_labs(page) -> None:
    errors_page = ErrorsPage(page)

    errors_page.open()
    errors_page.expect_page_ready()

    errors_page.network_fail_button.click()
    errors_page.trigger_timeouts()

    expect(errors_page.partial_good).to_be_visible()
    expect(errors_page.partial_fail).to_be_visible()

    # Leak growth is interval-driven, so wait for the displayed business signal
    # to change instead of asserting on an exact increment cadence.
    errors_page.start_leak()
    expect(errors_page.leak_status).not_to_contain_text("Leak size: 0")

    errors_page.run_security_labs()
    expect(errors_page.audit_log).to_contain_text("Audit log")
    expect(errors_page.security_headers_hint).to_be_visible()
