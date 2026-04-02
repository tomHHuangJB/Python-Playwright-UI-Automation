from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.a11y_page import A11yPage


@pytest.mark.regression
def test_a11y_announcements_and_focus_management(page) -> None:
    page.add_init_script(
        """
        Date.prototype.toLocaleTimeString = () => "10:30:00 AM";
        """
    )

    a11y_page = A11yPage(page)

    a11y_page.open()
    a11y_page.expect_page_ready()

    a11y_page.announce_update()
    expect(a11y_page.aria_live_region).to_contain_text("Update at 10:30:00 AM")

    a11y_page.open_modal()
    expect(a11y_page.focus_modal).to_be_visible()
    a11y_page.expect_modal_focused()

    a11y_page.close_modal()
    expect(a11y_page.focus_modal).to_have_count(0)

    expect(a11y_page.high_contrast_button).to_be_visible()
    expect(a11y_page.reduced_motion_button).to_be_visible()
