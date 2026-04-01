from __future__ import annotations

from playwright.sync_api import expect

from components.header import Header
from pages.base_page import BasePage


class AuthPage(BasePage):
    PATH = "/auth"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)

    @property
    def login_form(self):
        return self.by_test_id("login-form")

    @property
    def username_input(self):
        return self.by_test_id("login-username")

    @property
    def password_input(self):
        return self.by_test_id("login-password")

    @property
    def remember_me_checkbox(self):
        return self.by_test_id("login-remember")

    @property
    def login_submit_button(self):
        return self.by_test_id("login-submit")

    @property
    def auth_status(self):
        return self.by_test_id("auth-status")

    @property
    def mfa_code_input(self):
        return self.by_test_id("mfa-code")

    @property
    def mfa_verify_button(self):
        return self.by_test_id("mfa-verify")

    @property
    def oauth_google_button(self):
        return self.by_test_id("oauth-google")

    @property
    def oauth_facebook_button(self):
        return self.by_test_id("oauth-facebook")

    @property
    def session_refresh_card(self):
        return self.by_test_id("session-refresh")

    @property
    def session_concurrent_card(self):
        return self.by_test_id("session-concurrent")

    @property
    def session_sso_card(self):
        return self.by_test_id("session-sso")

    def open(self) -> None:
        self.goto(self.PATH)

    def expect_page_ready(self) -> None:
        self.header.expect_loaded()
        expect(self.login_form).to_be_visible()
        expect(self.mfa_code_input).to_be_visible()
        expect(self.oauth_google_button).to_be_visible()
        expect(self.session_refresh_card).to_be_visible()

    def login_as(self, username: str, password: str, remember_me: bool = False) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        if self.remember_me_checkbox.is_checked() != remember_me:
            self.remember_me_checkbox.click()
        self.login_submit_button.click()

    def submit_mfa(self, code: str) -> None:
        self.mfa_code_input.fill(code)
        self.mfa_verify_button.click()

    def expect_signed_in(self) -> None:
        expect(self.auth_status).to_contain_text("token:demo-token")

    def expect_mfa_refreshed(self) -> None:
        expect(self.auth_status).to_contain_text("refresh:refresh-rotated")

    def expect_session_controls(self) -> None:
        expect(self.session_refresh_card).to_contain_text("Token refresh rotation")
        expect(self.session_concurrent_card).to_contain_text("Concurrent sessions")
        expect(self.session_sso_card).to_contain_text("SSO logout")
