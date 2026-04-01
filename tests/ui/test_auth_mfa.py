import pytest

from flows.auth_flow import AuthFlow
from pages.auth_page import AuthPage


@pytest.mark.ui
def test_auth_mfa_refresh_flow(page) -> None:
    auth_page = AuthPage(page)
    auth_flow = AuthFlow(auth_page)

    auth_page.open()
    auth_page.expect_page_ready()
    auth_flow.sign_in_with_demo_user(remember_me=False)
    auth_flow.complete_mfa("123456")
