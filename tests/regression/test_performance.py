from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.performance_page import PerformancePage


@pytest.mark.regression
def test_performance_signals(page) -> None:
    performance_page = PerformancePage(page)

    performance_page.open()
    performance_page.expect_page_ready()

    # Large DOM rendering is variable, so wait for a meaningful threshold
    # rather than asserting on a precise mount timing.
    performance_page.wait_for_large_dom_render()
    assert performance_page.large_dom_count() > 100

    performance_page.block_main_thread()

    expect(performance_page.worker_result).to_contain_text("Result: 42")
    expect(performance_page.cpu_indicator).to_contain_text("Simulated CPU throttle: 4x")
    expect(performance_page.lazy_images.first).to_be_visible()
    expect(page.get_by_text("Performance marks available in performance entries.")).to_be_visible()
