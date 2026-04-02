from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.dynamic_page import DynamicPage


@pytest.mark.regression
def test_dynamic_async_behaviors(page) -> None:
    page.add_init_script(
        """
        Math.random = () => 0.9;
        Object.defineProperty(navigator, "serviceWorker", {
          configurable: true,
          value: {
            register: async () => ({ scope: "/sw.js" }),
            getRegistrations: async () => [{ unregister: async () => true }]
          }
        });
        """
    )

    dynamic_page = DynamicPage(page)

    dynamic_page.open()
    dynamic_page.expect_page_ready()

    dynamic_page.trigger_optimistic_update()
    dynamic_page.expect_optimistic_saved()
    expect(dynamic_page.dynamic_log).to_contain_text("Optimistic update confirmed")

    dynamic_page.trigger_race_requests()
    expect(dynamic_page.race_results).to_contain_text("fast:200ms")
    expect(dynamic_page.race_results).to_contain_text("slow:800ms")

    dynamic_page.trigger_dedup()
    expect(dynamic_page.dedup_status).to_contain_text("fresh -> cached")

    dynamic_page.trigger_partial_fetch()
    expect(dynamic_page.partial_status).to_contain_text("status:206")

    dynamic_page.toggle_consistency()
    expect(dynamic_page.consistency_status).to_contain_text("visibleAfter:2000ms")

    dynamic_page.register_service_worker()
    expect(dynamic_page.sw_status).to_contain_text("registered")

    dynamic_page.unregister_service_worker()
    expect(dynamic_page.sw_status).to_contain_text("unregistered")

    expect(dynamic_page.partial_failure).to_contain_text("Partial failure")
