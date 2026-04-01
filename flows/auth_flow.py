from __future__ import annotations

from pages.auth_page import AuthPage


class AuthFlow:
    def __init__(self, auth_page: AuthPage) -> None:
        self.auth_page = auth_page

    def sign_in_with_demo_user(self, remember_me: bool = True) -> None:
        self.auth_page.login_as("principal.engineer", "demo", remember_me=remember_me)
        self.auth_page.expect_signed_in()

    def complete_mfa(self, code: str = "123456") -> None:
        self.auth_page.submit_mfa(code)
        self.auth_page.expect_mfa_refreshed()
