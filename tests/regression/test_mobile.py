from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.mobile_page import MobilePage


@pytest.mark.regression
def test_mobile_orientation_gestures_and_refresh(page) -> None:
    page.set_viewport_size({"width": 430, "height": 932})

    mobile_page = MobilePage(page)

    mobile_page.open()
    mobile_page.expect_page_ready()

    expect(mobile_page.orientation_value).to_contain_text("portrait")

    page.set_viewport_size({"width": 932, "height": 430})
    expect(mobile_page.orientation_value).to_contain_text("landscape")

    mobile_page.swipe_right()
    expect(mobile_page.gesture_result).to_contain_text("swipe-right")

    mobile_page.trigger_long_press()
    expect(mobile_page.gesture_result).to_contain_text("long-press")

    expect(mobile_page.refresh_count).to_have_text("0")
    mobile_page.trigger_refresh()
    expect(mobile_page.refresh_count).to_have_text("1")
