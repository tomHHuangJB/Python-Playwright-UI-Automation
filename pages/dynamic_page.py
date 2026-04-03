from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class DynamicPage(BasePage):
    PATH = "/dynamic"
    ROUTE_NAME = "dynamic"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def optimistic_count(self):
        return self.by_test_id("optimistic-count")

    @property
    def optimistic_button(self):
        return self.by_test_id("optimistic-btn")

    @property
    def optimistic_status(self):
        return self.by_test_id("optimistic-status")

    @property
    def race_trigger(self):
        return self.by_test_id("race-trigger")

    @property
    def race_results(self):
        return self.by_test_id("race-results")

    @property
    def dedup_trigger(self):
        return self.by_test_id("dedup-trigger")

    @property
    def dedup_status(self):
        return self.by_test_id("dedup-status")

    @property
    def partial_trigger(self):
        return self.by_test_id("partial-trigger")

    @property
    def partial_status(self):
        return self.by_test_id("partial-status")

    @property
    def cache_toggle(self):
        return self.by_test_id("cache-toggle")

    @property
    def consistency_status(self):
        return self.by_test_id("consistency-status")

    @property
    def sw_register(self):
        return self.by_test_id("sw-register")

    @property
    def sw_unregister(self):
        return self.by_test_id("sw-unregister")

    @property
    def sw_status(self):
        return self.by_test_id("sw-status")

    @property
    def dynamic_log(self):
        return self.by_test_id("dynamic-log")

    @property
    def skeleton_card(self):
        return self.by_test_id("skeleton-card")

    @property
    def partial_failure(self):
        return self.by_test_id("partial-failure")

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.optimistic_button).to_be_visible()
        expect(self.race_trigger).to_be_visible()
        expect(self.skeleton_card).to_be_visible()

    def trigger_optimistic_update(self) -> None:
        self.optimistic_button.click()

    def expect_optimistic_saved(self) -> None:
        expect(self.optimistic_status).to_contain_text("saved")
        expect(self.optimistic_count).to_contain_text("1")

    def trigger_race_requests(self) -> None:
        self.race_trigger.click()

    def trigger_dedup(self) -> None:
        self.dedup_trigger.click()

    def trigger_partial_fetch(self) -> None:
        self.partial_trigger.click()

    def toggle_consistency(self) -> None:
        self.cache_toggle.click()

    def register_service_worker(self) -> None:
        self.sw_register.click()

    def unregister_service_worker(self) -> None:
        self.sw_unregister.click()
