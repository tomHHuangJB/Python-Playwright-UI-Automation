from __future__ import annotations

import pytest

from pages.home_page import HomePage
from utils.performance_utils import read_navigation_timing


@pytest.mark.perf
def test_home_navigation_timing_is_within_budget(page, settings) -> None:
    home_page = HomePage(page)

    home_page.open()
    home_page.expect_page_ready()

    timing = read_navigation_timing(page)

    # These are browser-side guardrails for obvious regressions on a local or CI
    # runner. They are intentionally conservative and are not a substitute for
    # load, stress, or capacity testing.
    assert timing.response_start_ms > 0
    assert timing.dom_content_loaded_ms <= settings.perf_dom_content_loaded_max_ms
    assert timing.load_event_ms <= settings.perf_navigation_max_ms
    assert timing.duration_ms <= settings.perf_navigation_max_ms
