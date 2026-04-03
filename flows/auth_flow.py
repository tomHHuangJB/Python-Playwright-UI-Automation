from __future__ import annotations

from fixtures.data_factory import DemoCredentials
from pages.auth_page import AuthPage


class AuthFlow:
    def __init__(self, auth_page: AuthPage) -> None:
        self.auth_page = auth_page

    def sign_in(self, credentials: DemoCredentials, remember_me: bool = True) -> None:
        self.auth_page.login_as(credentials.username, credentials.password, remember_me=remember_me)
        self.auth_page.expect_signed_in()

    def complete_mfa(self, code: str) -> None:
        self.auth_page.submit_mfa(code)
        self.auth_page.expect_mfa_refreshed()
