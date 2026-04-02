from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.integrations_page import IntegrationsPage


@pytest.mark.regression
def test_integrations_iframe_message_and_csp_surfaces(page) -> None:
    integrations_page = IntegrationsPage(page)

    integrations_page.open()
    integrations_page.expect_page_ready()

    integrations_page.approve_payment_in_iframe()
    expect(integrations_page.iframe_message).to_contain_text("Message from iframe: payment-approved")
    expect(integrations_page.csp_note).to_contain_text("CSP report-only endpoint should receive violations")
    expect(integrations_page.csp_iframe).to_have_attribute("title", "csp-test")
