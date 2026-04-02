from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class ErrorsPage(BasePage):
    PATH = "/errors"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def network_fail_button(self):
        return self.by_test_id("network-fail")

    @property
    def timeout_1s_button(self):
        return self.by_test_id("timeout-1s")

    @property
    def timeout_5s_button(self):
        return self.by_test_id("timeout-5s")

    @property
    def timeout_30s_button(self):
        return self.by_test_id("timeout-30s")

    @property
    def partial_good(self):
        return self.by_test_id("partial-good")

    @property
    def partial_fail(self):
        return self.by_test_id("partial-fail")

    @property
    def leak_start_button(self):
        return self.by_test_id("leak-start")

    @property
    def leak_status(self):
        return self.page.get_by_text("Leak size:")

    @property
    def security_injection_button(self):
        return self.by_test_id("security-injection")

    @property
    def security_access_button(self):
        return self.by_test_id("security-access")

    @property
    def security_xss_button(self):
        return self.by_test_id("security-xss")

    @property
    def security_vuln_button(self):
        return self.by_test_id("security-vuln")

    @property
    def security_ssrf_button(self):
        return self.by_test_id("security-ssrf")

    @property
    def security_crypto_button(self):
        return self.by_test_id("security-crypto")

    @property
    def security_logging_button(self):
        return self.by_test_id("security-logging")

    @property
    def audit_log(self):
        return self.by_test_id("audit-log")

    @property
    def security_headers_hint(self):
        return self.page.get_by_text("/api/security/headers")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.network_fail_button).to_be_visible()
        expect(self.timeout_1s_button).to_be_visible()
        expect(self.partial_good).to_be_visible()
        expect(self.leak_start_button).to_be_visible()

    def trigger_timeouts(self) -> None:
        self.timeout_1s_button.click()
        self.timeout_5s_button.click()
        self.timeout_30s_button.click()

    def start_leak(self) -> None:
        self.leak_start_button.click()

    def run_security_labs(self) -> None:
        self.security_injection_button.click()
        self.security_access_button.click()
        self.security_xss_button.click()
        self.security_vuln_button.click()
        self.security_ssrf_button.click()
        self.security_crypto_button.click()
        self.security_logging_button.click()
